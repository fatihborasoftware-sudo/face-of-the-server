cd /root/holo
declare -A COL=( [normal]='#6fdcff' [backup]='#39ff6a' [intrusion]='#ff2a1a' [heat]='#ff7a1a' [memory]='#b86bff' [ssd]='#ffb347' [load]='#e8f4ff' [update]='#4aa8ff' [alarm]='#ff4a3a' )
declare -A VO=( [normal]=tr-45fe61534c-f [backup]=tr-0fb15b14d6-f [intrusion]=tr-fc248319a7-f [heat]=tr-6eafac475e-f [memory]=tr-161d8e7b51-f [ssd]=tr-f1e5307901-f [load]=tr-b0191bd963-f [update]=tr-570374fe63-f [alarm]=tr-b16e056eb5-f )
declare -A NUM=( [normal]=0 [backup]=1 [intrusion]=2 [heat]=3 [memory]=4 [ssd]=5 [load]=6 [update]=7 [alarm]=8 )
mkdir -p out
for n in "$@"; do
  python3 rings.py $n "${COL[$n]}"
  ffmpeg -y -v error -framerate 30 -i S/${n}_r/f%04d.jpg -i /root/khoa/voice/${VO[$n]}.mp3 \
   -filter_complex "[0:v]curves=all='0/0 0.025/0 0.2/0.42 0.55/0.85 1/1',eq=saturation=1.3,fade=in:st=0:d=0.5,fade=out:st=19.3:d=0.7,format=yuv420p[v];[1:a]adelay=1900|1900,apad[a]" \
   -map "[v]" -map "[a]" -t 20 -c:v libx264 -preset slow -crf 17 -r 30 -c:a aac -b:a 160k -ar 44100 -movflags +faststart out/khoa-P30S-${NUM[$n]}-$n.mp4
  echo made $n
done
