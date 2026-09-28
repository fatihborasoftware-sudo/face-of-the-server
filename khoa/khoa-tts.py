#!/usr/bin/env python3
# khoa-tts.py - Khoa's voice: a tiny local web service on 127.0.0.1:8082 using the crew's Piper voices.
#   GET  /say?text=...&v=alan&len=1.0   -> audio/wav (cached)
#   GET  /voices                        -> the voice names it knows
#   POST /queue  text=...&sit=&title=&sub=&value=   -> queue a line for the Face page to speak (returns {"id":n})
#   GET  /queue?since=N                 -> queued lines with id > N (the page polls this)
#   GET  /queue?add=...&sit=...         -> same as POST, for a quick curl
import http.server, urllib.parse, subprocess, json, os, hashlib, struct, glob, sys, threading, time
PIPER='/srv/fb/shared/piper/piper/piper'; VOICES='/srv/fb/shared/piper/voices'
CACHE=os.environ.get('CACHE_DIRECTORY') or '/tmp/khoa-tts'; os.makedirs(CACHE,exist_ok=True)
Q=[]; QL=threading.Lock(); QN=[0]
def model(v):
    for c in glob.glob(f'{VOICES}/*{v}*.onnx'): return c
    return None
def rate(m):
    try: return json.load(open(m+'.json')).get('audio',{}).get('sample_rate',22050)
    except Exception: return 22050
def wav(raw,sr):
    return b'RIFF'+struct.pack('<I',36+len(raw))+b'WAVEfmt '+struct.pack('<IHHIIHH',16,1,1,sr,sr*2,2,16)+b'data'+struct.pack('<I',len(raw))+raw
def enqueue(q):
    text=(q.get('text',q.get('add',['']))[0]).strip()[:600]; sit=q.get('sit',[''])[0].strip(); title=q.get('title',[''])[0].strip()[:40]; sub=q.get('sub',[''])[0].strip()[:80]
    val=q.get('value',[''])[0].strip()
    if not text and not sit: return None
    with QL:
        QN[0]+=1; it={'id':QN[0],'text':text,'sit':sit,'title':title,'sub':sub,'t':time.time()}
        if val:
            try: it['value']=float(val)
            except ValueError: pass
        Q.append(it); del Q[:-50]
    return it
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self,*a): pass
    def send(self,code,body,ctype):
        self.send_response(code); self.send_header('Content-Type',ctype); self.send_header('Content-Length',str(len(body)))
        self.send_header('Access-Control-Allow-Origin','*'); self.send_header('Cache-Control','no-store'); self.end_headers(); self.wfile.write(body)
    def do_POST(self):
        u=urllib.parse.urlparse(self.path)
        if not u.path.endswith('/queue'): return self.send(404,b'no','text/plain')
        n=int(self.headers.get('Content-Length','0') or 0); body=self.rfile.read(n).decode('utf-8','replace')
        if (self.headers.get('Content-Type') or '').startswith('application/json'):
            try: q={k:[str(v)] for k,v in json.loads(body or '{}').items()}
            except Exception: q={}
        else: q=urllib.parse.parse_qs(body)
        it=enqueue(q)
        if not it: return self.send(400,b'bad request','text/plain')
        return self.send(200,json.dumps({'id':it['id']}).encode(),'application/json')
    def do_GET(self):
        u=urllib.parse.urlparse(self.path); q=urllib.parse.parse_qs(u.query)
        if u.path.endswith('/voices'):
            names=sorted(os.path.basename(p)[:-5] for p in glob.glob(VOICES+'/*.onnx')); return self.send(200,json.dumps(names).encode(),'application/json')
        if u.path.endswith('/queue'):
            if 'add' in q or ('text' in q and 'since' not in q):
                it=enqueue(q); return self.send(200 if it else 400,json.dumps({'id':it['id']} if it else {}).encode(),'application/json')
            try: since=int(q.get('since',['0'])[0])
            except ValueError: since=0
            with QL: items=[i for i in Q if i['id']>since]
            return self.send(200,json.dumps(items).encode(),'application/json')
        if not u.path.endswith('/say'): return self.send(404,b'no','text/plain')
        text=(q.get('text',[''])[0]).strip()[:600]; v=q.get('v',['alan'])[0]; ls=q.get('len',['1.0'])[0]
        m=model(v)
        if not text or not m: return self.send(400,b'bad request','text/plain')
        key=hashlib.sha1((v+'|'+ls+'|'+text).encode()).hexdigest(); f=f'{CACHE}/{key}.wav'
        if not os.path.exists(f):
            try:
                raw=subprocess.run([PIPER,'--model',m,'--length_scale',ls,'--output_raw'],input=(text+'\n').encode(),capture_output=True,timeout=60).stdout
            except Exception as e: return self.send(500,str(e).encode(),'text/plain')
            if not raw: return self.send(500,b'piper produced nothing','text/plain')
            open(f,'wb').write(wav(raw,rate(m)))
        return self.send(200,open(f,'rb').read(),'audio/wav')
if __name__=='__main__':
    port=int(sys.argv[1]) if len(sys.argv)>1 else 8082
    http.server.ThreadingHTTPServer(('127.0.0.1',port),H).serve_forever()
