# this is ../e/pointillist_maize/code/scaling_up/pointify.sh
#
mkdir -p ~/.config/rclone
cp /secrets/rclone.conf ~/.config/rclone
#
# make the persistent volume claim
#
mkdir /pvc/frames
rclone copy --progress nautilus:my-bucket/my-directory /pvc
#
# get the cuda ffmpeg needs
#
# export LD_LIBRARY_PATH="/usr/local/cuda-12.8/compat:$LD_LIBRARY_PATH"
# apt install libnvidia-decode-550-server
#
# run ffmpeg on whatever is in the directory and output the frames
#
ffmpeg -threads 0 -i /pvc/*.MOV -vf fps=2 /pvc/frames/24r_test_frame%06d.png
#
# move the output to safety and sleep
#
7z a -mmt /pvc/frames.zip /pvc/frames/*
rclone copy --progress /pvc/frames.7z nautilus:my-bucket
sleep infinity
