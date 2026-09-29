echo "$1" | /tmp/piper/piper --model /root/voices/en_GB-alan-medium.onnx --output_file /tmp/raw_en.wav >/dev/null 2>&1
ffmpeg -y -v error -i /tmp/raw_en.wav -ar 44100 "$2"
