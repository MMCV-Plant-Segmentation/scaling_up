import subprocess

class RCloneClient:
    def __init__(self):
        pass

    def upload(self, source_path, dest_bucket, dest_path):
        result = subprocess.run(
            ["rclone", "copy", "--progress", source_path, f"nautilus:{dest_bucket}/{dest_path}"],
            check=True,
        )
        return result
