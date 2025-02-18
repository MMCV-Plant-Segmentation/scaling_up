mkdir -p ~/.config/rclone
cp /secrets/rclone.conf ~/.config/rclone
mkdir /pvc/frames
rclone copy nautilus:my-bucket/my-directory /pvc
ffmpeg -i /pvc/*.MOV -vf fps=2 /pvc/frames/24r_test_frame%06d.png
zip /pvc/frames.zip /pvc/frames
rclone copy /pvc/frames.zip nautilus:my-bucket
sleep infinity
