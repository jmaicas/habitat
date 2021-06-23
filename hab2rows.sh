#!/bin/bash
set -o nounset
set -o errexit

declare -i hor=500
declare -i vert=445

for FILE in *.avi
do
  file=${FILE// /_}
  if [[ $FILE = *" "* ]]; then
    echo "the file name contains one or more spaces, changing them by _"
    mv "$FILE" "$file"
  fi  

  # creates a folder to store the rows of each file
  folder=${file%.avi}
  mkdir $folder


  # Row A
  ffmpeg -i $file -filter:v "crop=$hor:$vert:250:0" $folder/A4.avi;
  ffmpeg -i $file -filter:v "crop=$hor:$vert:1230:0" $folder/A3.avi;
  ffmpeg -i $file -filter:v "crop=$hor:$vert:2150:0" $folder/A2.avi;
  ffmpeg -i $file -filter:v "crop=$hor:$vert:3155:0" $folder/A1.avi;

  ffmpeg -i $folder/A4.avi -i $folder/A3.avi -i $folder/A2.avi -i $folder/A1.avi -filter_complex "
  nullsrc=size=2000x$vert [background];
  [0:v] setpts=PTS-STARTPTS, scale=$hor\x$vert [left];
  [1:v] setpts=PTS-STARTPTS, scale=$hor\x$vert [left-middle];
  [2:v] setpts=PTS-STARTPTS, scale=$hor\x$vert [right-middle];
  [3:v] setpts=PTS-STARTPTS, scale=$hor\x$vert [right];
  [background][left] overlay=shortest=1 [tmp1];
  [tmp1][left-middle] overlay=shortest=1:x=500 [tmp2];
  [tmp2][right-middle] overlay=shortest=1:x=1000 [tmp3];
  [tmp3][right] overlay=shortest=1:x=1500" $folder/A_$file

  rm $folder/A1.avi $folder/A2.avi $folder/A3.avi $folder/A4.avi

  # Row B
  ffmpeg -i $file -filter:v "crop=$hor:$vert:280:600" $folder/B4.avi;
  ffmpeg -i $file -filter:v "crop=$hor:$vert:1220:510" $folder/B3.avi;
  ffmpeg -i $file -filter:v "crop=$hor:$vert:2170:610" $folder/B2.avi;
  ffmpeg -i $file -filter:v "crop=$hor:$vert:3140:620" $folder/B1.avi;

  ffmpeg -i $folder/B4.avi -i $folder/B3.avi -i $folder/B2.avi -i $folder/B1.avi -filter_complex "
  nullsrc=size=2000x$vert [background];
  [0:v] setpts=PTS-STARTPTS, scale=$hor\x$vert [left];
  [1:v] setpts=PTS-STARTPTS, scale=$hor\x$vert [left-middle];
  [2:v] setpts=PTS-STARTPTS, scale=$hor\x$vert [right-middle];
  [3:v] setpts=PTS-STARTPTS, scale=$hor\x$vert [right];
  [background][left] overlay=shortest=1 [tmp1];
  [tmp1][left-middle] overlay=shortest=1:x=500 [tmp2];
  [tmp2][right-middle] overlay=shortest=1:x=1000 [tmp3];
  [tmp3][right] overlay=shortest=1:x=1500" $folder/B_$file

  rm $folder/B1.avi $folder/B2.avi $folder/B3.avi $folder/B4.avi

  # Row C
  ffmpeg -i $file -filter:v "crop=$hor:$vert:240:1120" $folder/C4.avi;
  ffmpeg -i $file -filter:v "crop=$hor:$vert:1200:1130" $folder/C3.avi;
  ffmpeg -i $file -filter:v "crop=$hor:$vert:2210:1130" $folder/C2.avi;
  ffmpeg -i $file -filter:v "crop=$hor:$vert:3170:1050" $folder/C1.avi;

  ffmpeg -i $folder/C4.avi -i $folder/C3.avi -i $folder/C2.avi -i $folder/C1.avi -filter_complex "
  nullsrc=size=2000x$vert [background];
  [0:v] setpts=PTS-STARTPTS, scale=$hor\x$vert [left];
  [1:v] setpts=PTS-STARTPTS, scale=$hor\x$vert [left-middle];
  [2:v] setpts=PTS-STARTPTS, scale=$hor\x$vert [right-middle];
  [3:v] setpts=PTS-STARTPTS, scale=$hor\x$vert [right];
  [background][left] overlay=shortest=1 [tmp1];
  [tmp1][left-middle] overlay=shortest=1:x=500 [tmp2];
  [tmp2][right-middle] overlay=shortest=1:x=1000 [tmp3];
  [tmp3][right] overlay=shortest=1:x=1500" $folder/C_$file

  rm $folder/C1.avi $folder/C2.avi $folder/C3.avi $folder/C4.avi

  # Row D
  ffmpeg -i $file -filter:v "crop=$hor:$vert:240:1620" $folder/D4.avi;
  ffmpeg -i $file -filter:v "crop=$hor:$vert:1180:1620" $folder/D3.avi;
  ffmpeg -i $file -filter:v "crop=$hor:$vert:2150:1640" $folder/D2.avi;
  ffmpeg -i $file -filter:v "crop=$hor:$vert:3130:1715" $folder/D1.avi;

  ffmpeg -i $folder/D4.avi -i $folder/D3.avi -i $folder/D2.avi -i $folder/D1.avi -filter_complex "
  nullsrc=size=2000x$vert [background];
  [0:v] setpts=PTS-STARTPTS, scale=$hor\x$vert [left];
  [1:v] setpts=PTS-STARTPTS, scale=$hor\x$vert [left-middle];
  [2:v] setpts=PTS-STARTPTS, scale=$hor\x$vert [right-middle];
  [3:v] setpts=PTS-STARTPTS, scale=$hor\x$vert [right];
  [background][left] overlay=shortest=1 [tmp1];
  [tmp1][left-middle] overlay=shortest=1:x=500 [tmp2];
  [tmp2][right-middle] overlay=shortest=1:x=1000 [tmp3];
  [tmp3][right] overlay=shortest=1:x=1500" $folder/D_$file

  rm $folder/D1.avi $folder/D2.avi $folder/D3.avi $folder/D4.avi
  
done
