# this is ../e/pointillist_maize/code/scaling_up/reconstruct.sh
#
mkdir -p ~/.config/rclone
cp /secrets/rclone.conf ~/.config/rclone
#
# make the persistent volume claim
#
#
colmap automatic_reconstructor --image_path /pvc/frames --workspace_path /pvc/colmapresult --data_type video --quality extreme --SiftExtraction.use_gpu 1 --SiftMatching.use_gpu 1
echo colmap did its thing maybe
sleep infinity
