#! /bin/bash

bfiles=()

arr=("0.00" "0.33" "0.67" "1.00")

# First we extract all base files :)
for file in ./*
do
    filename=$(basename "$file")
    ext="${filename##*.}"
    if [ "$ext" = "mp4" ]
    then
        fname="${filename%.*}"
        name="${fname#$"main-"}"
        bfiles+=($name)
        for vol in "${arr[@]}"
        do
            ffmpeg -y -i $filename -t 00:00:20 -vn -acodec libmp3lame \
                -ac 2 -ab 128k -ar 48000 -filter:a "volume=$vol" "$name-$vol.mp3"
        done
    fi
done



echo ${bfiles[@]}

