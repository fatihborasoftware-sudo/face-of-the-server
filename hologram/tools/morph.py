import numpy as np, cv2
W=768; rng=np.random.default_rng(3)
def pts(img_bgr, n, thr=40):
    lum=img_bgr.max(2); ys,xs=np.nonzero(lum>thr)
    if len(xs)==0: return np.zeros((n,2)),np.zeros((n,3))
    w=lum[ys,xs].astype(np.float64); w/=w.sum()
    idx=rng.choice(len(xs),n,p=w)
    return np.stack([xs[idx],ys[idx]],1).astype(np.float32), img_bgr[ys[idx],xs[idx]].astype(np.float32)
def ease(x): x=np.clip(x,0,1); return x*x*(3-2*x)
def morph(src, dst, k, n=9000, seed=5):
    """src,dst: BGR float32 images. k 0..1 : body -> dust -> gauge"""
    r=np.random.default_rng(seed)
    P,Cs=pts(src.astype(np.uint8),n); Q,Cd=pts(dst.astype(np.uint8),n)
    ang=r.uniform(0,2*np.pi,n); rad=r.uniform(120,380,n)
    mid=np.stack([384+np.cos(ang)*rad, 384+np.sin(ang)*rad*0.9],1)
    swirl=(k*5.0)
    a=ease(k/0.5); b=ease((k-0.45)/0.55)
    X=P*(1-a)+mid*a; X=X*(1-b)+Q*b
    # rotate around centre while in dust
    th=swirl*(1-b)*0.35; c,s=np.cos(th),np.sin(th); X=(X-384)@np.array([[c,-s],[s,c]])+384
    col=Cs*(1-b)+Cd*b
    out=np.zeros((W,W,3),np.float32)
    xi=np.clip(X[:,0].astype(int),0,W-1); yi=np.clip(X[:,1].astype(int),0,W-1)
    boost=1.0+1.8*np.sin(np.pi*min(1,k/0.95))
    for dy,dx in ((0,0),(1,0),(0,1),(1,1)):
        np.add.at(out,(np.clip(yi+dy,0,W-1),np.clip(xi+dx,0,W-1)),col*0.9*boost)
    out+=cv2.GaussianBlur(out,(0,0),3)*1.4
    base=src*(1-ease(k/0.3))*1.0 + dst*ease((k-0.8)/0.2)
    return np.clip(base+out,0,255)
