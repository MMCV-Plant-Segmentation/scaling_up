# this is <wherever you decided to clone this repo :)>/vggt_reconstruct.sh

mkdir -p ~/.config/rclone
cp /secrets/rclone.conf ~/.config/rclone

mkdir results

rclone copy --progress nautilus:my-bucket/frames.tar .
tar xvf frames.tar

sleep infinity
