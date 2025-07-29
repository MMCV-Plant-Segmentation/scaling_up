import hashlib
import json
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
    job_response = client.create_job(manifest_path)
    job_name = job_response['metadata']['name']
    event_stream = client.get_events(watch=True, watch_only=True)
    pod_name = None

    for event in event_stream:
        # if event['involvedObject']['name'] != job_name:
        if not event['involvedObject']['name'].startswith(job_name):
            continue

        # TODO: not working for reconstruction for some reason? nautilus update?
        # reason = event['reason']
        # print(reason, event['message'])
        # if reason == 'SuccessfulCreate':
        #     match = re.match('Created pod: (.*)', event['message'])
        #     pod_name = match.groups()[0]
        #     break

        pod_name = event['involvedObject']['name']
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
    log_stream = client.get_logs(f"Pod/{pod_name}", follow=True)
    for line in log_stream:
        print('>', line, end='')
    print("End of logs")

    final_status = client.get_pod(pod_name, watch_pod=False)
    return final_status


def upload_video(client: RCloneClient, video_path: Path, bucket, destination_folder: str):
    client.upload(str(video_path), bucket, destination_folder)
    return f"{destination_folder}/{video_path.name}"


def download_reconstruction(client: RCloneClient, bucket, reconstruction_path: str, destination_folder: Path):
    client.download(bucket, reconstruction_path, str(destination_folder))

def get_reconstruction_from_video(source_video_path: Path, output_reconstruction_folder: Path):
    with open(source_video_path, 'rb') as f:
        hash = hash_file(f)
    video_id = hash.hexdigest()[:8]
    job_s3_folder = video_id

    bucket = "plant-segmentation"
    frames_archive_file_name = "frames.tar"
    reconstruction_archive_file_name = "reconstruction.tar"

    client = KubernetesClient()
    rclone_client = RCloneClient()

    destination = upload_video(rclone_client, source_video_path, bucket, job_s3_folder)

    job_name = f"reconstruction-{video_id}-{int(time.time())}"
    job_builder = ManifestBuilder(
        bucket_name=bucket,
        s3_folder_path=job_s3_folder,
        job_name=job_name,
        video_file_name=source_video_path.name,
        frames_archive_file_name=frames_archive_file_name,
        reconstruction_archive_file_name=reconstruction_archive_file_name,
    )
    extraction_manifest_path = job_builder.get_extraction_manifest()
    reconstruction_manifest_path = job_builder.get_reconstruction_manifest()

    try:
        # run_job(client, extraction_manifest_path)
        # run_job(client, reconstruction_manifest_path)
        pass
    except KubernetesApiError as e:
        traceback.print_tb(e.__traceback__)
        print()
        print(f"$ {' '.join(e.command)}")
        print(e.message)

    download_reconstruction(rclone_client, bucket, f"{job_s3_folder}/")


def main():
    video_path = Path("/home/creallf/Videos/not_DJI_0309.MOV")
    get_reconstruction_from_video(video_path)


if __name__ == '__main__':
    main()
