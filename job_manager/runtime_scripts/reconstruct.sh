BUCKET_NAME=$1
JOB_FOLDER_PATH=$2
FRAMES_ARCHIVE_FILE_NAME=$3
RECONSTRUCTION_ARCHIVE_FILE_NAME=$4

FRAMES_FILE_PATH="${JOB_FOLDER_PATH}/${FRAMES_ARCHIVE_FILE_NAME}"

mkdir -p ~/.config/rclone
cp /secrets/rclone.conf ~/.config/rclone
mkdir colmapresult

rclone copy --progress "${BUCKET_NAME}:${FRAMES_FILE_PATH}" .
tar xvf "${FRAMES_ARCHIVE_FILE_NAME}"
echo colmap automatic_reconstructor --image_path frames --workspace_path colmapresult --data_type video --quality extreme --num_threads=24

tar -cvf "${RECONSTRUCTION_ARCHIVE_FILE_NAME}" colmapresult
rclone copy --progress "${RECONSTRUCTION_ARCHIVE_FILE_NAME}" "nautilus:${BUCKET_NAME}/${JOB_FOLDER_PATH}"
