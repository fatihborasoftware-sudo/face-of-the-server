import cv2, numpy as np, sys, os, math
name, color = sys.argv[1], sys.argv[2]
c=tuple(int(color[i:i+2],16) for i in (5,3,1))  # BGR
src=f'S/{name}'; out=f'S/{name}_r'; os.makedirs(out,exist_ok=True)
files=sorted(f for f in os.listdir(src) if f.endswith('.jpg'))
W=768; C=(384,384); FPS=30
def arcs(img,r,n,gap,rot,th,col,a):
    seg=360/n
    for k in range(n):
        s=rot+k*seg; cv2.ellipse(img,C,(r,r),0,s,s+seg-gap,col,th,cv2.LINE_AA)
for i,f in enumerate(files):
    t=i/FPS
    fr=cv2.imread(f'{src}/{f}').astype(np.float32)
    ov=np.zeros((W,W,3),np.float32)
    on=min(1,max(0,(t-1.0)/0.8))            # rings grow in with the situation
    base=0.35+0.65*on
    col=np.array(c,np.float32)*base
    arcs(ov,int(360-6*(1-on)),24,6,t*14,2,col.tolist(),1)
    arcs(ov,int(346),6,38,-t*22,3,(col*0.8).tolist(),1)
    arcs(ov,int(372),72,3.2,t*6,1,(col*0.6).tolist(),1)
    # scanning sweep dot
    a=math.radians(t*95); p=(int(384+353*math.cos(a)),int(384+353*math.sin(a)))
    cv2.circle(ov,p,4,(255,255,255),-1,cv2.LINE_AA)
    # pulse ring on situation start
    if 1.0<=t<=2.6:
        k=(t-1.0)/1.6; r=int(60+300*k); cv2.circle(ov,C,r,(col*(1-k)*1.3).tolist(),2,cv2.LINE_AA)
    glow=cv2.GaussianBlur(ov,(0,0),5)*1.4
    img=np.clip(fr+ov+glow,0,255).astype(np.uint8)
    cv2.imwrite(f'{out}/{f}',img,[cv2.IMWRITE_JPEG_QUALITY,95])
print('rings',name,len(files))
