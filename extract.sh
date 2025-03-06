# this is ../e/pointillist_maize/code/scaling_up/extract.sh
#
mkdir -p ~/.config/rclone
cp /secrets/rclone.conf ~/.config/rclone
# make pvc
mkdir /pvc/frames /pvc/colmapresult
rclone copy --progress nautilus:my-bucket/my-directory /pvc
#
#
#
# run ffmpeg on whatever is in the directory and output the frames
#
ffmpeg -threads 0 -i /pvc/*.MOV -vf fps=2 /pvc/frames/24r_test_frame%06d.png
#
# move the output to safety and sleep
#
tar -cvf /pvc/frames.tar /pvc/frames/*
sleep infinity
