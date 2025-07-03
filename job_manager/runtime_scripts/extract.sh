VIDEO_BUCKET_NAME=$1
VIDEO_FILE_PATH=$2
VIDEO_FOLDER_PATH="$(dirname $VIDEO_FILE_PATH)"
VIDEO_FILE_NAME="$(basename $VIDEO_FILE_PATH)"
VIDEO_NAME="${VIDEO_FILE_NAME%.*}"

mkdir -p ~/.config/rclone
cp /secrets/rclone.conf ~/.config/rclone

mkdir frames
rclone copy --progress "nautilus:$VIDEO_BUCKET/$VIDEO_FILE_PATH" .

ffmpeg -threads 0 -progress - -i "$VIDEO_FILE_NAME" -vf fps=2 "frames/$VIDEO_NAME%06d.png"

tar -cvf "$VIDEO_NAME-frames.tar" frames/*
rclone copy --progress "$VIDEO_NAME-frames.tar" "nautilus:$VIDEO_BUCKET/$VIDEO_FOLDER_PATH"
