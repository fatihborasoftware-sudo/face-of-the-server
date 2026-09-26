#!/usr/bin/env python3
"""
build_body.py — turn any .glb model into the compact body data that index.html embeds.

What it does
  1. reads the GLB (positions, normals, indices, base-colour texture if present)
  2. optionally crops it (keep only vertices above --ycut, e.g. waist up)
  3. decimates by vertex clustering (finer on the head, coarser on the body)
  4. normalises the model to the page's coordinate space (height ≈ 2.9 units, y up, x/z centred)
  5. quantises positions (uint16), normals (int8) and a "tendon/whiteness" byte from the texture
  6. writes body-data.js  — or injects the data straight into index.html with --inject

Usage
  python3 tools/build_body.py model.glb                       # writes body-data.js next to the model
  python3 tools/build_body.py model.glb --ycut -7 --inject index.html
  python3 tools/build_body.py model.glb --head-y 13 --head-span 4 --body-cell 0.33 --head-cell 0.13

Needs: numpy, pillow  (pip install numpy pillow)

The page expects, in this order inside one base64 blob:
  uint16[NV*3] positions (quantised between LO and HI) · int8[NV*3] normals · uint8[NV] tendon · uint16[NTRI*3] indices
and the constants LO, HI, NV, NTRI. Keep NV below 65536 so the indices fit in uint16.
"""
import argparse, base64, io, json, re, struct, sys
import numpy as np

def read_glb(path):
    f = open(path, 'rb').read()
    magic, ver, length = struct.unpack('<III', f[:12])
    assert magic == 0x46546C67, 'not a GLB file'
    off, chunks = 12, []
    while off < len(f):
        cl, ct = struct.unpack('<II', f[off:off + 8]); chunks.append((ct, f[off + 8:off + 8 + cl])); off += 8 + cl
    js = json.loads(chunks[0][1]); bin_ = chunks[1][1]
    return js, bin_

def accessor(js, bin_, i):
    a = js['accessors'][i]; bv = js['bufferViews'][a['bufferView']]
    ct = {5126: np.float32, 5125: np.uint32, 5123: np.uint16, 5121: np.uint8}[a['componentType']]
    n = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4}[a['type']]
    start = bv.get('byteOffset', 0) + a.get('byteOffset', 0)
    return np.frombuffer(bin_, dtype=ct, count=a['count'] * n, offset=start).reshape(a['count'], n)

def node_matrices(js):
    """world matrix per mesh index (walks the scene graph)."""
    W = {}
    nodes = js['nodes']
    def walk(i, M):
        n = nodes[i]
        m = np.array(n.get('matrix', list(np.eye(4).flatten('F'))), dtype=np.float64).reshape(4, 4, order='F')
        if 'translation' in n or 'rotation' in n or 'scale' in n:
            t = n.get('translation', [0, 0, 0]); s = n.get('scale', [1, 1, 1]); x, y, z, w = n.get('rotation', [0, 0, 0, 1])
            R = np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                          [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                          [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])
            m = np.eye(4); m[:3, :3] = R * np.array(s); m[:3, 3] = t
        Mw = M @ m
        if 'mesh' in n: W[n['mesh']] = Mw
        for c in n.get('children', []): walk(c, Mw)
    for r in js['scenes'][js.get('scene', 0)]['nodes']: walk(r, np.eye(4))
    return W

def load_image(js, bin_, idx):
    try:
        from PIL import Image
        im = js['images'][idx]; bv = js['bufferViews'][im['bufferView']]
        d = bin_[bv.get('byteOffset', 0):bv.get('byteOffset', 0) + bv['byteLength']]
        return np.asarray(Image.open(io.BytesIO(d)).convert('RGB'))
    except Exception:
        return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('glb')
    ap.add_argument('--ycut', type=float, default=None, help='drop everything below this model-space y (e.g. -7 = waist up)')
    ap.add_argument('--head-y', type=float, default=None, help='model-space y where the head starts (default: top 30%%)')
    ap.add_argument('--head-span', type=float, default=None, help='blend distance below head-y')
    ap.add_argument('--body-cell', type=float, default=0.33, help='cluster cell on the body, in model units (bigger = fewer vertices)')
    ap.add_argument('--head-cell', type=float, default=0.13, help='cluster cell on the head')
    ap.add_argument('--height', type=float, default=2.9, help='page-space height of the result')
    ap.add_argument('--bottom', type=float, default=-1.9, help='page-space y of the lowest vertex')
    ap.add_argument('--out', default=None, help='output .js (default: body-data.js beside the glb)')
    ap.add_argument('--inject', default=None, help='index.html to patch in place')
    a = ap.parse_args()

    js, bin_ = read_glb(a.glb); W = node_matrices(js)
    P, N, C, T, base = [], [], [], [], 0
    for mi, m in enumerate(js['meshes']):
        Mw = W.get(mi, np.eye(4)); R = Mw[:3, :3]
        for p in m['primitives']:
            pos = accessor(js, bin_, p['attributes']['POSITION']).astype(np.float64) @ R.T + Mw[:3, 3]
            if 'NORMAL' in p['attributes']:
                nrm = accessor(js, bin_, p['attributes']['NORMAL']).astype(np.float64) @ np.linalg.inv(R).T
            else:
                nrm = np.zeros_like(pos); nrm[:, 2] = 1
            nrm /= np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-9
            col = np.full((len(pos), 3), 170, dtype=np.uint8)
            mat = js['materials'][p['material']] if 'material' in p else {}
            pbr = mat.get('pbrMetallicRoughness', {})
            if 'baseColorTexture' in pbr and 'TEXCOORD_0' in p['attributes']:
                px = load_image(js, bin_, js['textures'][pbr['baseColorTexture']['index']]['source'])
                if px is not None:
                    h, w = px.shape[:2]; uv = accessor(js, bin_, p['attributes']['TEXCOORD_0'])
                    u = (np.mod(uv[:, 0], 1) * (w - 1)).astype(int); v = (np.mod(uv[:, 1], 1) * (h - 1)).astype(int); col = px[v, u]
            idx = accessor(js, bin_, p['indices']).reshape(-1, 3).astype(np.int64) + base if 'indices' in p else np.arange(len(pos)).reshape(-1, 3) + base
            P.append(pos); N.append(nrm); C.append(col); T.append(idx); base += len(pos)
    P = np.vstack(P); N = np.vstack(N); C = np.vstack(C); T = np.vstack(T)
    print(f'read {len(P)} vertices, {len(T)} triangles, bounds y {P[:,1].min():.2f}..{P[:,1].max():.2f}')

    if a.ycut is not None:
        T = T[(P[T, 1] > a.ycut).all(1)]
    lo_y, hi_y = P[T, 1].min(), P[T, 1].max()
    head_y = a.head_y if a.head_y is not None else hi_y - 0.30 * (hi_y - lo_y)
    span = a.head_span if a.head_span is not None else 0.12 * (hi_y - lo_y)

    # vertex clustering, finer on the head
    head = np.clip((P[:, 1] - head_y) / span, 0, 1)
    cell = a.body_cell - (a.body_cell - a.head_cell) * head
    key = np.floor((P - P.min(0)) / cell[:, None]).astype(np.int64); zone = (head * 8).astype(np.int64)
    kid = (key[:, 0] * 1000003 + key[:, 1] * 1009 + key[:, 2]) * 16 + zone
    uniq, inv = np.unique(kid, return_inverse=True); nv = len(uniq)
    V = np.zeros((nv, 3)); Nn = np.zeros((nv, 3)); Cc = np.zeros((nv, 3)); cnt = np.zeros(nv)
    np.add.at(V, inv, P); np.add.at(Nn, inv, N); np.add.at(Cc, inv, C); np.add.at(cnt, inv, 1)
    V /= cnt[:, None]; Nn /= np.linalg.norm(Nn, axis=1, keepdims=True) + 1e-9; Cc /= cnt[:, None]
    T2 = inv[T]; T2 = T2[(T2[:, 0] != T2[:, 1]) & (T2[:, 1] != T2[:, 2]) & (T2[:, 0] != T2[:, 2])]
    used = np.unique(T2); remap = -np.ones(nv, dtype=np.int64); remap[used] = np.arange(len(used))
    T2 = remap[T2]; V = V[used]; Nn = Nn[used]; Cc = Cc[used]
    print(f'decimated to {len(V)} vertices, {len(T2)} triangles')
    if len(V) >= 65536:
        sys.exit('too many vertices for uint16 indices — raise --body-cell (e.g. 0.4) and run again')

    # normalise to page space
    lo = V.min(0); hi = V.max(0); s = a.height / (hi[1] - lo[1])
    Vn = np.stack([(V[:, 0] - (lo[0] + hi[0]) / 2) * s, (V[:, 1] - lo[1]) * s + a.bottom, (V[:, 2] - (lo[2] + hi[2]) / 2) * s], 1)
    LO = Vn.min(0); HI = Vn.max(0)
    q = np.round((Vn - LO) / (HI - LO) * 65535).astype(np.uint16)
    qn = np.clip(np.round(Nn * 127), -127, 127).astype(np.int8)
    lum = Cc.mean(1); red = Cc[:, 0] - Cc[:, 1]
    tendon = np.clip((lum - 150) / 100, 0, 1) * (red < 50)
    k = np.round(tendon * 255).astype(np.uint8)
    blob = q.tobytes() + qn.tobytes() + k.tobytes() + T2.astype(np.uint16).tobytes()
    b64 = base64.b64encode(blob).decode()
    consts = f'const LO=[{LO[0]:.5f},{LO[1]:.5f},{LO[2]:.5f}], HI=[{HI[0]:.5f},{HI[1]:.5f},{HI[2]:.5f}], NV={len(V)}, NTRI={len(T2)};'
    print(f'data: {len(blob)/1e6:.2f} MB raw, {len(b64)/1e6:.2f} MB base64')

    if a.inject:
        html = open(a.inject, encoding='utf-8').read()
        html, n1 = re.subn(r'const ECO="[^"]*";', 'const ECO="' + b64 + '";', html, count=1)
        html, n2 = re.subn(r'const LO=\[[^\]]*\], HI=\[[^\]]*\], NV=\d+, NTRI=\d+;', consts, html, count=1)
        if n1 != 1 or n2 != 1: sys.exit('could not find the ECO / LO-HI lines in ' + a.inject)
        open(a.inject, 'w', encoding='utf-8').write(html); print('injected into', a.inject)
    else:
        out = a.out or re.sub(r'\.glb$', '', a.glb) + '-body-data.js'
        open(out, 'w', encoding='utf-8').write('// generated by tools/build_body.py — paste these two lines into index.html\nconst ECO="' + b64 + '";\n' + consts + '\n')
        print('wrote', out)

if __name__ == '__main__':
    main()
