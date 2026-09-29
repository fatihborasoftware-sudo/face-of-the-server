import numpy as np, cv2, math
from PIL import Image, ImageDraw, ImageFont
W=768; FPS=30; DUR=9.0; N=int(DUR*FPS)
rng=np.random.default_rng(7)
logo=Image.open('logo.png').convert('RGBA'); LW=640; LH=round(logo.height*LW/logo.width)
logo=logo.resize((LW,LH),Image.LANCZOS); L=np.asarray(logo).astype(np.float32)/255
LX=(W-LW)//2; LY=350-LH//2
# sample particles from logo
ys,xs=np.nonzero(L[:,:,3]>0.5); idx=rng.choice(len(xs),size=min(16000,len(xs)),replace=False)
tx=xs[idx]+LX+rng.normal(0,.3,len(idx)); ty=ys[idx]+LY+rng.normal(0,.3,len(idx))
col=L[ys[idx],xs[idx],:3]; col=np.clip(col*1.25+0.08,0,1)
M=len(idx)
# start: swirling disc
r0=rng.uniform(60,420,M)**1.0; a0=rng.uniform(0,2*np.pi,M)
delay=rng.uniform(0,1.1,M)+ (tx-LX)/LW*0.5
dx=rng.normal(0,1,M); dy=rng.normal(-0.6,1,M)
tag='BUILD · LEARN · HOST · CREATE'
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf',22)
def ease(x): x=np.clip(x,0,1); return 1-(1-x)**3
def sm(a,b,t): x=min(max((t-a)/(b-a),0),1); return x*x*(3-2*x)
for f in range(N):
    t=f/FPS
    acc=np.zeros((W,W,3),np.float32)
    # converge 0.3..3.6
    p=ease((t-0.3-delay)/2.4)
    ang=a0 + (1-p)*(2.2+t*0.9)
    sx=W/2+np.cos(ang)*r0*(1-p)*1.0; sy=W/2+np.sin(ang)*r0*0.55*(1-p)
    x=sx*(1-p)+tx*p; y=sy*(1-p)+(ty)*p
    # dissolve 7.4..9
    d=max(0,t-7.4); x=x+dx*d*d*38; y=y+dy*d*d*38
    bright=sm(0,0.8,t)*(1-sm(7.6,8.9,t))
    # particles fade as solid logo takes over, then come back for dissolve
    pa=bright*(1-0.75*sm(3.5,4.2,t)+0.75*sm(7.2,7.5,t))
    xi=np.round(x).astype(int); yi=np.round(y).astype(int); ok=(xi>=0)&(xi<W)&(yi>=0)&(yi<W)
    np.add.at(acc,(yi[ok],xi[ok]),col[ok]*pa*0.9)
    # solid logo
    la=sm(3.4,4.2,t)*(1-sm(7.2,7.6,t))
    glow=cv2.GaussianBlur(acc,(0,0),6)*1.6+cv2.GaussianBlur(acc,(0,0),18)*0.9
    acc=acc+glow
    if la>0:
        lg=np.zeros_like(acc); lg[LY:LY+LH,LX:LX+LW]=L[:,:,:3]*L[:,:,3:4]*la
        acc+=cv2.GaussianBlur(lg,(0,0),14)*0.55
        region=acc[LY:LY+LH,LX:LX+LW]
        a=L[:,:,3:4]*la
        sweep=0
        s=(t-4.4)/0.9
        if 0<=s<=1:
            gx=np.arange(LW)[None,:]; gy=np.arange(LH)[:,None]
            band=np.exp(-((gx+gy*0.5-(s*(LW+LH)-LH*0.5))/40.0)**2)
            sweep=band[:,:,None]*0.9
        region[:]= region*(1-a)+ (L[:,:,:3]*1.05+sweep)*a
    img=np.clip(acc,0,1)
    im=Image.fromarray((img*255).astype(np.uint8))
    # tagline typing 4.6..6.2
    ta=(1-sm(7.2,7.6,t))
    n=int(len(tag)*min(1,max(0,(t-4.6)/1.6)))
    if n>0 and ta>0:
        dr=ImageDraw.Draw(im); s=tag[:n]; tw=dr.textlength(tag,font=font); x0=(W-tw)/2
        c=tuple(int(v*ta) for v in (111,220,255)); dr.text((x0,LY+LH+34),s,font=font,fill=c)
    im.save(f'la/f{f:04d}.jpg',quality=95)
print('ok',M)
