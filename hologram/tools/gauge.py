import numpy as np, cv2, math
from PIL import Image, ImageDraw, ImageFont
W=768; C=(384,384)
def hexbgr(h): return tuple(int(h[i:i+2],16) for i in (5,3,1))
def gauge(value, maxv, col_hex, unit='%', t=0.0, fill=1.0, label_value=None):
    col=np.array(hexbgr(col_hex),np.float32)
    img=np.zeros((W,W,3),np.float32)
    R=250
    # outer tick ring
    for k in range(120):
        a=math.radians(k*3+t*8); r1=292; r2=300 if k%5 else 312
        p1=(int(C[0]+r1*math.cos(a)),int(C[1]+r1*math.sin(a))); p2=(int(C[0]+r2*math.cos(a)),int(C[1]+r2*math.sin(a)))
        cv2.line(img,p1,p2,(col*0.55).tolist(),2 if k%5==0 else 1,cv2.LINE_AA)
    cv2.circle(img,C,R,(col*0.16).tolist(),20,cv2.LINE_AA)          # dark track
    cv2.circle(img,C,214,(col*0.35).tolist(),1,cv2.LINE_AA)
    cv2.circle(img,C,322,(col*0.25).tolist(),1,cv2.LINE_AA)
    frac=max(0,min(1,value/maxv))*fill
    start=135; sweep=270*frac
    cv2.ellipse(img,C,(R,R),0,start,start+sweep,col.tolist(),18,cv2.LINE_AA)
    # bright head on the arc
    a=math.radians(start+sweep); hp=(int(C[0]+R*math.cos(a)),int(C[1]+R*math.sin(a)))
    if frac>0.01: cv2.circle(img,hp,11,(255,255,255),-1,cv2.LINE_AA)
    # ECG heartbeat line across the circle
    xs=np.arange(40,W-40); ys=np.full(xs.shape,C[1]+60.0)
    beat=(t*1.2)%1.0
    for bx in [0.30,0.62,0.94]:
        cx=40+((bx+beat)%1.0)*(W-80)
        d=xs-cx
        ys+= -95*np.exp(-(d/6)**2) + 40*np.exp(-((d-12)/6)**2) - 18*np.exp(-((d+26)/10)**2)
    pts=np.stack([xs,ys],1).astype(np.int32)
    fade=np.clip(1-np.abs(xs-C[0])/360,0,1)**0.6
    for i in range(len(pts)-1):
        cv2.line(img,tuple(pts[i]),tuple(pts[i+1]),(col*fade[i]).tolist(),3,cv2.LINE_AA)
    glow=cv2.GaussianBlur(img,(0,0),7)*1.5+cv2.GaussianBlur(img,(0,0),22)*0.8
    img=np.clip(img+glow,0,255)
    im=Image.fromarray(cv2.cvtColor(img.astype(np.uint8),cv2.COLOR_BGR2RGB))
    if label_value is not False:
        d=ImageDraw.Draw(im); f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf',96)
        s=(label_value if isinstance(label_value,str) else f'{int(round(value))}{unit}')
        tw=d.textlength(s,font=f); rgb=tuple(int(col_hex[i:i+2],16) for i in (1,3,5))
        glowt=Image.new('RGB',(W,W)); ImageDraw.Draw(glowt).text(((W-tw)/2,C[1]-110),s,font=f,fill=rgb)
        g=cv2.GaussianBlur(np.asarray(glowt).astype(np.float32),(0,0),9)*1.2
        base=np.asarray(im).astype(np.float32)+g
        im=Image.fromarray(np.clip(base,0,255).astype(np.uint8)); ImageDraw.Draw(im).text(((W-tw)/2,C[1]-110),s,font=f,fill=(235,255,245))
    return im
if __name__=='__main__':
    gauge(82,100,'#39ff6a',t=0.3).save('g_test.png')
