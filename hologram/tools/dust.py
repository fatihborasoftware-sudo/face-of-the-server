import cv2, numpy as np, os, math
FPS=30; W=768; rng=np.random.default_rng(11)
BOX=(84,70,684,670)   # framing A (zoom 1.28) on the 768 render
# speech intervals and mode colours (hex) ; before 20 s = normal cyan
L=[(7.8,2.98,'#6fdcff'),(11.6,7.37,'#6fdcff'),(20.0,2.80,'#39ff6a'),(23.8,5.36,'#ff2a1a'),(30.2,3.42,'#ff7a1a'),(34.6,3.11,'#b86bff'),(38.7,3.45,'#ffb347'),(43.1,2.69,'#4aa8ff'),(46.8,6.69,'#6fdcff')]
def hx(h): return np.array([int(h[i:i+2],16) for i in (5,3,1)],np.float32)  # BGR
def talk(t):
    a=0
    for s,d,_ in L:
        a=max(a, min(1,max(0,(t-s+0.4)/0.8))*min(1,max(0,(s+d+1.2-t)/1.2)))
    return a
def colour(t):
    c=hx('#6fdcff'); cur=c
    for s,d,h in L:
        k=min(1,max(0,(t-(s-0.2))/0.8)); cur=cur*(1-k)+hx(h)*k
    return cur
M=240
px=rng.uniform(0,W,M); py=rng.uniform(0,W,M)
ph=rng.uniform(0,2*np.pi,(M,4)); fr=rng.uniform(0.15,0.6,(M,4)); sz=rng.uniform(0.8,2.4,M); tw=rng.uniform(0.5,2.0,M)
src='en_fr'; out='en_out'; os.makedirs(out,exist_ok=True)
files=sorted(f for f in os.listdir(src) if f.endswith('.jpg'))
for i,f in enumerate(files):
    t=i/FPS
    im=cv2.imread(f'{src}/{f}')[BOX[1]:BOX[3],BOX[0]:BOX[2]]
    im=cv2.resize(im,(W,W),interpolation=cv2.INTER_CUBIC).astype(np.float32)
    a=talk(t); speed=0.35+1.6*a
    vx=(np.sin(ph[:,0]+t*fr[:,0])+0.6*np.sin(ph[:,1]+t*fr[:,1]*2.3))*speed*1.1
    vy=(np.cos(ph[:,2]+t*fr[:,2])+0.6*np.cos(ph[:,3]+t*fr[:,3]*1.9))*speed*1.1-0.15*speed
    px=(px+vx)%W; py=(py+vy)%W
    ov=np.zeros((W,W,3),np.float32); col=colour(t)
    vis=(0.18+0.82*a)*min(1,t/6.5)
    for j in range(M):
        tws=0.55+0.45*math.sin(t*tw[j]*3+ph[j,0])
        cv2.circle(ov,(int(px[j]),int(py[j])),int(round(sz[j])),(col*tws*vis).tolist(),-1,cv2.LINE_AA)
    ov+=cv2.GaussianBlur(ov,(0,0),4)*1.5
    cv2.imwrite(f'{out}/{f}',np.clip(im+ov,0,255).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,94])
print('dust',len(files))
