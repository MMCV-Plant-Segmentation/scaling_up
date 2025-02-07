mkdir -p ~/.config/rclone
cp /secrets/rclone.conf ~/.config/rclone
mkdir /pvc/raw
rclone copy nautilus:my-bucket/my-directory /pvc
ffmpeg -i /pvc/*.MOV -vf fps=2 /pvc/raw/24r_test_frame%06d.png
sleep infinity
