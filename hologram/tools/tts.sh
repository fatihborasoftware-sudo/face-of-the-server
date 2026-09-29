# $1 text, $2 out.mp3
echo "$1" | /tmp/piper/piper --model /root/voices/tr_TR-dfki-medium.onnx --length_scale 1.12 --noise_scale 0.33 --noise_w 0.4 --sentence_silence 0.3 --output_file /tmp/raw.wav 2>/dev/null
ffmpeg -y -v error -i /tmp/raw.wav -af "asetrate=22050*0.8409,aresample=22050,atempo=1/0.8409,equalizer=f=180:t=q:w=1:g=3,aecho=0.8:0.6:28|55:0.25|0.15,equalizer=f=3000:t=q:w=1:g=2" -ar 44100 "$2"
