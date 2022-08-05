for file in ${AUDIO_DATAROOT}/*.ogg; do
    ffmpeg -y -i ${file} -ac 1 -ar 16000  ${WAV_DATAROOT}/$(basename ${file%.ogg}.wav)
done