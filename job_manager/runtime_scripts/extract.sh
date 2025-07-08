BUCKET_NAME=$1
JOB_FOLDER_PATH=$2
VIDEO_FILE_NAME=$3
FRAMES_ARCHIVE_FILE_NAME=$4

VIDEO_FILE_PATH="${JOB_FOLDER_PATH}/${VIDEO_FILE_NAME}"
VIDEO_NAME="${VIDEO_FILE_NAME%.*}"

mkdir -p ~/.config/rclone
cp /secrets/rclone.conf ~/.config/rclone

mkdir frames
rclone copy --progress "nautilus:${BUCKET_NAME}/${VIDEO_FILE_PATH}" .

ffmpeg -threads 0 -progress - -i "${VIDEO_FILE_NAME}" -vf fps=2 "frames/${VIDEO_NAME}%06d.png"

tar -cvf "${FRAMES_ARCHIVE_FILE_NAME}" frames/*
rclone copy --progress "${FRAMES_ARCHIVE_FILE_NAME}" "nautilus:${BUCKET_NAME}/${JOB_FOLDER_PATH}"
