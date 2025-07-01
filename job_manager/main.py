import re
import traceback
import pathlib

from extractor_manifest_builder import VideoExtractorJobBuilder
from kubernetes_client import KubernetesApiError, KubernetesClient
from rclone_client import RCloneClient


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


def upload_video(video_path):
    # TODO: video file names are not unique across years - need to do something about that!
    video_path = pathlib.Path(video_path)
    bucket = "plant-segmentation"
    destination = video_path.stem

    rclone = RCloneClient()
    rclone.upload(str(video_path), bucket, destination)
    return bucket, f"{destination}/{video_path.name}"

def main():
    bucket, destination = upload_video("/home/creallf/Videos/not_DJI_0309.MOV")
    client = KubernetesClient()
    job_builder = VideoExtractorJobBuilder(bucket, destination, client)
    manifest_path = job_builder.build()

    run_job(client, manifest_path)

if __name__ == '__main__':
    main()
