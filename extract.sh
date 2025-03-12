# this is ../e/pointillist_maize/code/scaling_up/extract.sh
#
mkdir -p ~/.config/rclone
cp /secrets/rclone.conf ~/.config/rclone
# make pvc
mkdir /home/ubuntu/frames
rclone copy --progress nautilus:my-bucket/my-directory /home/ubuntu
#
#
#
# run ffmpeg on whatever is in the directory and output the frames
#
ffmpeg -threads 0 -progress - -i /home/ubuntu/*.MOV -vf fps=2 /home/ubuntu/frames/24r_test_frame%06d.png
#
# move the output to safety and sleep
#
tar -cvf /home/ubuntu/frames.tar /home/ubuntu/frames/*
rclone copy --progress /home/ubuntu/frames.tar nautilus:my-bucket
sleep infinity
