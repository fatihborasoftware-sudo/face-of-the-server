import sys, os, json, math
sys.path.insert(0,'/root/holo')
import numpy as np, cv2
from gauge import gauge
MODE=sys.argv[1]; SRC={'talk':'g_talk','idle':'g_idle','natural':'g_natural','look':'g_look'}[MODE]; OUT=f'c_{MODE}'
os.makedirs(OUT,exist_ok=True)
FPS=30; W=768; BOX=(84,70,684,670)
TL=json.load(open(f'timeline_{MODE}.json'))
N=int(round(TL['dur']*FPS))
def hx(h): return np.array([int(h[i:i+2],16) for i in (5,3,1)],np.float32)
COL={'normal':'#6fdcff','backup':'#39ff6a','intrusion':'#ff2a1a','heat':'#ff7a1a','memory':'#b86bff','ssd':'#ffb347','update':'#4aa8ff'}
G={'backup':(0,100,100,'%',None),'intrusion':(0,48,60,'',None),'heat':(48,93,100,'°C',None),'memory':(41,97,100,'%',None),'ssd':(31,96,100,'%',None),'update':(0,27,27,'','x/27')}
def ease(x): x=np.clip(x,0,1); return x*x*(3-2*x)
def curve(a):
    x=a/255.0; x=np.interp(x,[0,0.025,0.2,0.55,1],[0,0,0.42,0.85,1]); return (x*255).astype(np.float32)
cache={}
def khoa(i):
    i=max(0,min(N-1,i))
    if i in cache: return cache[i]
    im=cv2.imread(f'{SRC}/f{i:04d}.jpg')[BOX[1]:BOX[3],BOX[0]:BOX[2]]
    im=curve(cv2.resize(im,(W,W),interpolation=cv2.INTER_CUBIC).astype(np.float32))
    if len(cache)>6: cache.clear()
    cache[i]=im; return im
def gimg(mode,rel,t):
    v0,v1,mx,u,lab=G[mode]; v=v0+(v1-v0)*ease((rel-2.0)/3.0)
    im=gauge(v,mx,COL[mode],unit=u,t=t,label_value=(f'{int(round(v))}/27' if lab else None))
    return cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2BGR).astype(np.float32)
def sample(img,n,seed):
    r=np.random.default_rng(seed); lum=img.max(2); ys,xs=np.nonzero(lum>40)
    w=lum[ys,xs].astype(np.float64); w/=w.sum(); idx=r.choice(len(xs),n,p=w)
    return np.stack([xs[idx],ys[idx]],1).astype(np.float32), img[ys[idx],xs[idx]].astype(np.float32)
def splat(P,C,k,boost=1.0):
    out=np.zeros((W,W,3),np.float32); xi=np.clip(P[:,0].astype(int),0,W-2); yi=np.clip(P[:,1].astype(int),0,W-2)
    for dy,dx in ((0,0),(1,0),(0,1),(1,1)): np.add.at(out,(yi+dy,xi+dx),C*0.9*boost)
    return out+cv2.GaussianBlur(out,(0,0),3)*1.4
MORPH={}
def morph(key,srcimg,dstimg,src_live,dst_live,k,n=9000):
    if key not in MORPH:
        r=np.random.default_rng(abs(hash(key))%1000)
        P,Cs=sample(srcimg,n,1); Q,Cd=sample(dstimg,n,2)
        ang=r.uniform(0,2*np.pi,n); rad=r.uniform(120,370,n)
        MORPH[key]=(P,Cs,Q,Cd,np.stack([384+np.cos(ang)*rad,384+np.sin(ang)*rad*0.92],1))
    P,Cs,Q,Cd,mid=MORPH[key]
    a=ease(k/0.5); b=ease((k-0.45)/0.55)
    X=P*(1-a)+mid*a; X=X*(1-b)+Q*b
    th=k*1.6*(1-b); c,s=math.cos(th),math.sin(th); X=(X-384)@np.array([[c,-s],[s,c]],np.float32)+384
    col=Cs*(1-b)+Cd*b; boost=1.0+1.8*math.sin(math.pi*min(1,k/0.95))
    base=src_live*(1-ease(k/0.3))+dst_live*ease((k-0.8)/0.2)
    return base+splat(X,col,k,boost)
def dissolve(key,srcimg,src_live,k,n=9000):
    if key not in MORPH:
        r=np.random.default_rng(9); P,Cs=sample(srcimg,n,3)
        ang=r.uniform(0,2*np.pi,n); rad=r.uniform(140,420,n)
        MORPH[key]=(P,Cs,np.stack([384+np.cos(ang)*rad,384+np.sin(ang)*rad],1))
    P,Cs,mid=MORPH[key]; a=ease(k/0.7); X=P*(1-a)+mid*a
    th=k*1.2; c,s=math.cos(th),math.sin(th); X=(X-384)@np.array([[c,-s],[s,c]],np.float32)+384
    fade=1-ease((k-0.35)/0.65)
    return src_live*(1-ease(k/0.3))+splat(X,Cs,k,(1.0+1.6*math.sin(math.pi*min(1,k)))*fade)
# ---- ambient dust
rng=np.random.default_rng(11); M=240
px=rng.uniform(0,W,M); py=rng.uniform(0,W,M); ph=rng.uniform(0,2*np.pi,(M,4)); fr=rng.uniform(0.15,0.6,(M,4)); sz=rng.uniform(0.8,2.4,M); tw=rng.uniform(0.5,2.0,M)
says=TL.get('says',[]); sits=TL.get('sits',[])
def talk(t):
    a=0
    for s in says: a=max(a,min(1,max(0,(t-s['t']+0.4)/0.8))*min(1,max(0,(s['t']+s['d']+1.2-t)/1.2)))
    return a
def colour(t):
    cur=hx(COL['normal'])
    for s in sits:
        k=min(1,max(0,(t-s['t'])/0.8)); cur=cur*(1-k)+hx(COL[s['name']])*k
    return cur
segs=TL.get('segs',[])
for i in range(N):
    t=i/FPS; img=None
    for sg in segs:
        rel=t-sg['start']; m=sg['mode']; key=m
        if 1.0<=rel<2.2:
            f0=int(round((sg['start']+1.0)*FPS)); snap_g=gimg(m,2.2,sg['start']+2.2)
            img=morph(key+'out',khoa(f0),snap_g,khoa(i),gimg(m,rel,t),(rel-1.0)/1.2)
        elif 2.2<=rel<5.4:
            img=gimg(m,rel,t)
        elif 5.4<=rel<6.6:
            f1=int(round((sg['start']+6.6)*FPS))
            img=morph(key+'back',gimg(m,5.4,sg['start']+5.4),khoa(f1),gimg(m,rel,t),khoa(i),(rel-5.4)/1.2)
    DS=TL.get('dissolve',25.0 if MODE=='idle' else None)
    if DS is not None:
        if DS<=t<DS+3.4: img=dissolve('out',khoa(int(DS*FPS)),khoa(i),(t-DS)/3.4)
        elif t>=DS+3.4: img=np.zeros((W,W,3),np.float32)
    if img is None: img=khoa(i)
    # ambient dust
    a=talk(t); speed=0.35+1.6*a
    vx=(np.sin(ph[:,0]+t*fr[:,0])+0.6*np.sin(ph[:,1]+t*fr[:,1]*2.3))*speed*1.1
    vy=(np.cos(ph[:,2]+t*fr[:,2])+0.6*np.cos(ph[:,3]+t*fr[:,3]*1.9))*speed*1.1-0.15*speed
    px=(px+vx)%W; py=(py+vy)%W
    ov=np.zeros((W,W,3),np.float32); col=colour(t); vis=(0.2+0.8*a)*min(1,t/5.0)
    for j in range(M):
        tws=0.55+0.45*math.sin(t*tw[j]*3+ph[j,0])
        cv2.circle(ov,(int(px[j]),int(py[j])),int(round(sz[j])),(col*tws*vis).tolist(),-1,cv2.LINE_AA)
    ov+=cv2.GaussianBlur(ov,(0,0),4)*1.5
    cv2.imwrite(f'{OUT}/f{i:04d}.jpg',np.clip(img+ov,0,255).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,94])
print('comp',MODE,N)
