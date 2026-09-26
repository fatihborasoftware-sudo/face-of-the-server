// ---------- webcam: the figure looks at whoever is in front of the camera (feeds window.serraLookAt)
(() => {
  const bar=document.querySelector('.bar'); if(!bar) return;
  const btn=document.createElement('button'); btn.id='cam'; btn.textContent='◉ CAMERA'; bar.insertBefore(btn,document.getElementById('stop'));
  const video=document.createElement('video'); video.setAttribute('playsinline',''); video.muted=true; video.style.cssText='position:fixed;right:-9999px;bottom:0;width:1px;height:1px;opacity:0';
  document.body.appendChild(video);
  const cv=document.createElement('canvas'); cv.width=64; cv.height=48; const cx2=cv.getContext('2d',{willReadFrequently:true});
  let stream=null, fd=null, mode='off', prev=null, face={x:0.5,y:0.45,t:0}, timer=0, busy=false;
  const gaze=document.getElementById('gaze');
  const secure=location.protocol==='https:'||/^(localhost|127\.0\.0\.1)$/.test(location.hostname);
  function say(t){ if(gaze) gaze.textContent=t; }
  function loadScript(u){ return new Promise((ok,err)=>{ const s=document.createElement('script'); s.src=u; s.onload=ok; s.onerror=err; document.head.appendChild(s); }); }
  async function start(){
    if(!navigator.mediaDevices||!navigator.mediaDevices.getUserMedia){ say('CAMERA · NOT AVAILABLE IN THIS BROWSER'); return; }
    if(!secure){ say('CAMERA · NEEDS HTTPS OR THE SERVER SCREEN (LOCALHOST)'); return; }
    try{ stream=await navigator.mediaDevices.getUserMedia({video:{width:{ideal:320},height:{ideal:240},facingMode:'user'},audio:false}); }
    catch(e){ say('CAMERA · PERMISSION REFUSED ('+(e.name||e)+')'); return; }
    video.srcObject=stream; await video.play();
    mode='motion';
    try{ if(!window.FaceDetection) await loadScript('https://cdn.jsdelivr.net/npm/@mediapipe/face_detection/face_detection.js');
      fd=new FaceDetection({locateFile:f=>'https://cdn.jsdelivr.net/npm/@mediapipe/face_detection/'+f}); fd.setOptions({model:'short',minDetectionConfidence:0.5});
      fd.onResults(r=>{ busy=false; const d=r.detections&&r.detections[0]; if(d){ const b=d.boundingBox; face={x:b.xCenter,y:b.yCenter,t:performance.now()}; } });
      await fd.initialize(); mode='face'; }catch(e){ fd=null; mode='motion'; }
    window.fbCamOn=true; btn.classList.add('on'); btn.textContent='◉ CAMERA ON'; try{localStorage.setItem('fbCam','1');}catch(e){}
    timer=setInterval(step, mode==='face'?140:100);
  }
  function stop(){ window.fbCamOn=false; clearInterval(timer); timer=0; if(stream){ stream.getTracks().forEach(t=>t.stop()); stream=null; } mode='off'; btn.classList.remove('on'); btn.textContent='◉ CAMERA'; try{localStorage.removeItem('fbCam');}catch(e){} say('LOOKING AT · MOUSE'); }
  function step(){
    if(video.readyState<2) return;
    if(mode==='face'&&fd){ if(!busy){ busy=true; fd.send({image:video}).catch(()=>{busy=false;}); } }
    else { // motion fallback: centre of what changed since the last frame
      cx2.drawImage(video,0,0,64,48); const d=cx2.getImageData(0,0,64,48).data; if(prev){ let sx=0,sy=0,n=0;
        for(let i=0;i<d.length;i+=4){ const diff=Math.abs(d[i]-prev[i])+Math.abs(d[i+1]-prev[i+1])+Math.abs(d[i+2]-prev[i+2]); if(diff>60){ const p=i>>2; sx+=p%64; sy+=(p/64)|0; n++; } }
        if(n>12){ face={x:(sx/n+0.5)/64, y:(sy/n+0.5)/48, t:performance.now()}; } }
      prev=new Uint8ClampedArray(d); }
    // apply: the camera looks at the viewer, so image-right is the viewer's left (mirror)
    if(performance.now()-face.t<2500){ const nx=(0.5-face.x)*3.6, ny=(face.y-0.5)*3.2; if(window.serraLookAt) window.serraLookAt(Math.max(-1,Math.min(1,nx)),Math.max(-1,Math.min(1,ny)));
      say('LOOKING AT · YOU (CAMERA'+(mode==='face'?' · FACE)':' · MOTION)')); }
  }
  btn.onclick=e=>{ e.stopPropagation(); if(mode==='off') start(); else stop(); };
  let auto=false; try{ auto=localStorage.getItem('fbCam')==='1'||/[?&]cam/.test(location.search); }catch(e){}
  if(auto) setTimeout(start,1500);
  window.fbCamera={start,stop};
})();
