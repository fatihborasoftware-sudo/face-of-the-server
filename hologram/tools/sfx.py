import numpy as np, json, wave, math
SR=44100
TL=json.load(open('/root/holo/timeline_natural.json'))
DUR=TL['dur']; N=int(DUR*SR)
L=np.zeros(N); R=np.zeros(N)
rng=np.random.default_rng(21)
def add(sig,t,vol=1.0,pan=0.0):
    i=int(t*SR); j=min(N,i+len(sig))
    if i>=N or j<=i: return
    s=sig[:j-i]*vol
    L[i:j]+=s*math.sqrt((1-pan)/2); R[i:j]+=s*math.sqrt((1+pan)/2)
def env(n,a=0.01,r=0.2):
    e=np.ones(n); na=max(1,int(a*SR)); nr=max(1,int(r*SR))
    e[:na]=np.linspace(0,1,na); e[-nr:]*=np.linspace(1,0,nr); return e
def lp(x,a):  # one-pole lowpass, a = smoothing 0..1 (array or scalar)
    y=np.zeros_like(x); acc=0.0; a=np.broadcast_to(a,x.shape)
    for i in range(len(x)): acc+=a[i]*(x[i]-acc); y[i]=acc
    return y
def sweep_noise(d,f0,f1,vol=1.0):
    n=int(d*SR); x=rng.normal(0,1,n); f=np.geomspace(f0,f1,n); a=1-np.exp(-2*np.pi*f/SR)
    y=lp(x,a); y=y-lp(y,np.full(n,1-np.exp(-2*np.pi*120/SR)))
    return y/ (np.abs(y).max()+1e-9)*vol*env(n,0.05,0.25)
def tone(d,f0,f1=None,type='sine',decay=None,vol=1.0):
    n=int(d*SR); f1=f0 if f1 is None else f1; f=np.geomspace(f0,f1,n) if f0>0 and f1>0 else np.full(n,f0)
    ph=2*np.pi*np.cumsum(f)/SR
    y=np.sin(ph) if type=='sine' else (2*((ph/(2*np.pi))%1)-1 if type=='saw' else np.sign(np.sin(ph)))
    e=env(n,0.004,min(0.1,d*0.3))
    if decay: e*=np.exp(-np.arange(n)/SR/decay)
    return y*e*vol
def ping(freqs,d=1.2,decay=0.35,vol=0.5):
    return sum(tone(d,f,decay=decay*(1-0.15*k),vol=vol/(k+1)) for k,f in enumerate(freqs))
# --- ambient drone
t=np.arange(N)/SR
drone=0.05*np.sin(2*np.pi*55*t)*(0.7+0.3*np.sin(2*np.pi*0.07*t))+0.03*np.sin(2*np.pi*82.5*t+0.5*np.sin(2*np.pi*0.11*t))+0.018*np.sin(2*np.pi*110.3*t)
wash=lp(rng.normal(0,1,N),np.full(N,1-np.exp(-2*np.pi*400/SR)))*0.05*(0.6+0.4*np.sin(2*np.pi*0.05*t+1))
fade=np.minimum(1,t/3)*np.minimum(1,(DUR-t)/2)
L+= (drone+wash*0.8)*fade; R+=(drone+wash*1.2)*fade
# --- morph in: real assemble sound
def readwav(p):
    w=wave.open(p); d=np.frombuffer(w.readframes(w.getnframes()),np.int16).reshape(-1,w.getnchannels())/32768.0; return d
A=readwav('/root/holo/assemble.wav'); add(A[:,0]*0.85,0.0,1.0,-0.1); add(A[:,1]*0.85,0.0,1.0,0.1) if A.shape[1]>1 else None
PITCH={'backup':(523,784),'intrusion':(440,415),'heat':(392,370),'memory':(587,880),'ssd':(494,740),'update':(659,988)}
for sg in TL['segs']:
    s=sg['start']; m=sg['mode']; a,b=PITCH[m]
    # colour change: scan chime (glide) + soft sparkle
    add(tone(0.5,a,b,vol=0.18)*np.linspace(1,0.2,int(0.5*SR)),s+0.2,1,-0.3); add(tone(0.6,b*2,b*2.01,vol=0.08,decay=0.25),s+0.35,1,0.3)
    # morph out: rising whoosh + granular sparkle
    add(sweep_noise(1.3,300,7000,0.35),s+0.95,1,0)
    for k in range(40):
        tt=s+1.0+rng.uniform(0,1.1); add(tone(0.05,rng.uniform(2500,6000),decay=0.02,vol=0.06),tt,1,rng.uniform(-0.8,0.8))
    # lock-in: sub thud + metallic ping
    add(tone(0.7,70,28,vol=0.55,decay=0.25),s+2.2,1,0); add(ping([1318,2093,3136,4186],1.6,0.45,0.35),s+2.2,1,0.1)
    add(sweep_noise(0.25,8000,1500,0.18),s+2.15,1,0)
    # ring fill: servo rising + ticks
    d=2.9; n=int(d*SR); srv=tone(d,180,540,'saw',vol=0.06); srv=lp(srv,np.full(n,0.08))*3*env(n,0.2,0.4); add(srv,s+2.3,1,-0.2)
    for k in range(int(2.8/0.09)): add(tone(0.012,3200,vol=0.07),s+2.3+k*0.09,1,0.4*math.sin(k))
    # heartbeat blips during gauge
    for k in range(4): add(tone(0.09,880,860,vol=0.14,decay=0.05),s+2.5+k*0.833,1,0); add(tone(0.07,660,vol=0.07,decay=0.04),s+2.62+k*0.833,1,0)
    if m=='intrusion':
        for k in range(6): add(tone(0.18,720 if k%2==0 else 960,type='square',vol=0.05),s+2.4+k*0.45,1,0.5 if k%2 else -0.5)
    if m=='heat': add(lp(rng.normal(0,1,int(3*SR)),np.full(int(3*SR),0.02))*2.5*env(int(3*SR),0.5,1.0),s+2.3,0.25,0)
    if m=='update':
        for k in range(8): add(tone(0.06,1200+k*120,vol=0.06,decay=0.03),s+2.4+k*0.35,1,0.3)
    # value reached: confirm chirp
    add(tone(0.12,b*1.5,b*2,vol=0.1),s+5.05,1,0)
    # morph back: falling whoosh + reform arpeggio
    add(sweep_noise(1.2,6000,250,0.3),s+5.4,1,0)
    for k,f in enumerate([a,a*1.26,a*1.5,a*2]): add(tone(0.35,f,decay=0.2,vol=0.08),s+6.3+k*0.07,1,-0.4+0.25*k)
# --- dissolve at end: reversed assemble
Ar=A[::-1,0][int(2.2*SR):int(6.2*SR)]*0.6*env(int(4*SR),0.3,1.2); add(Ar,TL['dissolve'],1,0)
M=np.stack([L,R],1); M/= max(1e-9,np.abs(M).max()/0.92)
w=wave.open('/root/holo/natural_sfx.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((M*32767).astype(np.int16).tobytes()); w.close()
print('sfx ok',DUR)
