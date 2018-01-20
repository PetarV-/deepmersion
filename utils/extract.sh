#! /bin/bash

bfiles=()

# If one would like to add volumes, they could do so here.
# For our prototype, we will either play full-volume or silent
arr=("1.00")

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

for class in ${bfiles[@]}
do
  echo $class >> 'classes.txt'
done

