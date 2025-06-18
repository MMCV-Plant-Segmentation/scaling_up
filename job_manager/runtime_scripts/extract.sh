VIDEO_FILE_NAME = $1

mkdir -p ~/.config/rclone
cp /secrets/rclone.conf ~/.config/rclone

mkdir /home/ubuntu/frames
rclone copy --progress "nautilus:my-bucket/my-directory/$VIDEO_FILE_NAME" /home/ubuntu

ffmpeg -threads 0 -progress - -i "/home/ubuntu/$VIDEO_FILE_NAME" -vf fps=2 "/home/ubuntu/frames/$VIDEO_FILE_NAME%06d.png"

tar -cvf frames.tar frames/*
rclone copy --progress /home/ubuntu/$VIDEO_FILE_NAME-frames.tar nautilus:my-bucket
