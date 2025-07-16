import hashlib
import re
import time
import traceback

from pathlib import Path

from manifest_builder import ManifestBuilder
from kubernetes_client import KubernetesApiError, KubernetesClient
from rclone_client import RCloneClient

def hash_file(f):
    # https://stackoverflow.com/a/59056837/11411686
    hash = hashlib.md5()
    while chunk := f.read(8192):
        hash.update(chunk)

    return hash


def run_job(client, manifest_path):
    try:
        job_response = client.create_job(manifest_path)
        job_name = job_response['metadata']['name']
        event_stream = client.get_events(watch=True, resource=f"job/{job_name}") # watch_only=True
        pod_name = None

        for event in event_stream:
            if event['involvedObject']['name'] != job_name:
                continue

            reason = event['reason']
            print(reason, event['message'])
            if reason == 'SuccessfulCreate':
                match = re.match('Created pod: (.*)', event['message'])
                pod_name = match.groups()[0]
                break

        state_stream = client.get_pod(pod_name, watch=True)
        for state in state_stream:
            phase = state['status']['phase']
            print(f"Waiting for pod '{pod_name}' to start. Current status is: {phase}")
            if phase != 'Pending':
                print(f"Status {phase} is not Pending, done waiting!")
                break

        print(f"Fetching logs for pod '{pod_name}'")
        print("=" * 20)
        log_stream = client.get_logs(f"Pod/{pod_name}", True)
        for line in log_stream:
            print(line, end='')

    except KubernetesApiError as e:
        traceback.print_tb(e.__traceback__)
        print()
        print(f"$ {' '.join(e.command)}")
        print(e.message)

    return "path/to/logs" # TODO


def upload_video(video_path: Path, bucket, destination_folder):
    rclone = RCloneClient()
    rclone.upload(str(video_path), bucket, destination_folder)
    return f"{destination_folder}/{video_path.name}"

def main():
    video_path = Path("/home/creallf/Videos/not_DJI_0309.MOV")
    with open(video_path, 'rb') as f:
        hash = hash_file(f)
    video_id = hash.hexdigest()[:8]
    job_s3_folder = video_id

    bucket = "plant-segmentation"
    destination = upload_video(video_path, bucket, job_s3_folder)

    client = KubernetesClient()
    job_name = f"reconstruction-{video_id}-{int(time.time())}"
    job_builder = ManifestBuilder(
        bucket_name=bucket,
        s3_folder_path=job_s3_folder,
        job_name=job_name,
        video_file_name=video_path.name,
        frames_archive_file_name="frames.tar",
        reconstruction_archive_file_name="reconstruction.tar",
    )
    extraction_manifest_path = job_builder.get_extraction_manifest()
    reconstruction_manifest_path = job_builder.get_reconstruction_manifest()

    run_job(client, reconstruction_manifest_path)

if __name__ == '__main__':
    main()
