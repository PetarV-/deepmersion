#!/usr/bin/env bash

# Convert mp4 audio files to ogg
# see: https://bytefreaks.net/gnulinux/bash/ffmpeg-extract-audio-from-mp4-to-ogg
for FILE in *.mp4;
do
    ffmpeg -loglevel panic -i "${FILE}" -vn -acodec libvorbis -y "${FILE%.mp4}.ogg" &
done

wait

