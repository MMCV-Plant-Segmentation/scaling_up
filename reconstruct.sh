# this is ../e/pointillist_maize/code/scaling_up/reconstruct.sh
#
mkdir -p ~/.config/rclone
cp /secrets/rclone.conf ~/.config/rclone
mkdir colmapresult

#Get frames from S3 storage
rclone copy --progress nautilus:my-bucket/frames.tar /home/ubuntu
#extract tar
tar xvf /home/ubuntu/frames.tar
#run colmap
colmap automatic_reconstructor --image_path /home/ubuntu/frames --workspace_path /home/ubuntu/colmapresult --data_type video --quality extreme --num_threads=24
