# this is ../e/pointillist_maize/code/scaling_up/reconstruct.sh
#
mkdir -p ~/.config/rclone
cp /secrets/rclone.conf ~/.config/rclone
mkdir colmapresult

#Get frames from S3 storage
rclone copy nautilus:my-bucket/frames.tar /home/ubuntu
#extract tar
tar xf /home/ubuntu/frames.tar --directory /home/ubuntu
#run colmap
colmap automatic_reconstructor --image_path /home/ubuntu/frames --workspace_path /home/ubuntu/colmapresult --data_type video --quality extreme --num_threads=18
echo colmap did its thing maybe
sleep infinity
