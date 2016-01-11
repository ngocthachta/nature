#!/bin/bash
# This bash scrip will convert flac files to alac files for playing in iphone devices
# it take all flac files from a input directory and convert to alac files into 
# output directory

if [ $# -lt 2 ]; then
    echo "Usage : flac_2_alac from_dir to_dir"
    exit 1
fi

if [ ! -d $2 ]; then
    echo "$2 does not exist. Make it !"
    mkdir -p $2
fi

for f in $1/*.flac; do ffmpeg -i "$f" -c:a alac "${f%.*}.m4a"; done

mv $1/*.m4a $2
exit 0
