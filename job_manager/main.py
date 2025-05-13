import traceback

from event_stream import EventStream
from job import Job
from extractor_manifest_builder import VideoExtractorJobBuilder
from kubernetes_client import KubernetesApiError, KubernetesClient


def main():
    client = KubernetesClient()
    job_builder = VideoExtractorJobBuilder("video.mov", client)
    manifest_path = job_builder.build()
    event_stream = EventStream(client)
    try:
        job_def = client.create_job(manifest_path)
        job_name = job_def['metadata']['name']
        job = Job(client, event_stream, job_name)

        for event in event_stream.get_events():
            # print(event['reason'], event['message'])
            pass

    except KubernetesApiError as e:
        traceback.print_tb(e.__traceback__)
        print()
        print(f"$ {' '.join(e.command)}")
        print(e.message)

if __name__ == '__main__':
    main()
