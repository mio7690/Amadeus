for file in ${AUDIO_DATAROOT}/*.ogg; do
    ffmpeg -y -i ${file} -ac 1 -ar 22050  -v quiet ${WAV_DATAROOT}/$(basename ${file%.ogg}.wav)
done