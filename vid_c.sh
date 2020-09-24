#!/bin/bash

inputfile=inputs
outputfile=outputs
while getopts "i:o:" flag; do
	case "${flag}" in
		i) inputfile=${OPTARG};;
		o) outputfile=${OPTARG};;
	esac
done

if [ ! -d $inputfile -o ! -d $outputfile ]; then
	echo $inputfile OR $outputfile directories do not exist
	exit
fi

for filename in $inputfile/*.{mp4,mov}; do
	ffmpeg -y -i "$filename" -vcodec libx264 -vf "scale='-2:min(720,ih)'" -crf 28 $outputfile/cc_"$(basename $filename)" || continue
done

du -hs $inputfile $outputfile

