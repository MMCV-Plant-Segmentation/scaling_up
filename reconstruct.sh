# this is ../e/pointillist_maize/code/scaling_up/reconstruct.sh
#
mkdir -p ~/.config/rclone
cp /secrets/rclone.conf ~/.config/rclone
#
# make the persistent volume claim
#
#
colmap automatic_reconstructor --image_path /pvc/frames --workspace_path /pvc/colmapresult --data_type video --quality extreme --num_threads=18
echo colmap did its thing maybe
sleep infinity
