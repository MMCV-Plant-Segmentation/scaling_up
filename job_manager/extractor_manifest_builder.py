import pathlib
import time
import random

from jinja2 import (
    Environment,
    FileSystemLoader,
)


# since apparently this isn't the default
def deterministic_hash(string):
    # https://stackoverflow.com/a/72059189/11411686
    r = random.Random(string) # oh the irony
    return r.randint(0, 9999999999) # that should be a low enough chance of collisions for our purposes


class VideoExtractorJobBuilder:
    def __init__(self, video_bucket, video_path, kubernetes_client):
        self.video_bucket = video_bucket
        self.video_path = video_path
        self.id = deterministic_hash(self.video_path)
        self.name = f"reconstruction-{self.id}-{int(time.time())}"
        self.kubernetes_client = kubernetes_client

    # TODO: extract this into a class to avoid recreating the environment
    def create_extraction_manifest(self, output_path: str, job_name: str, bucket: str, video: str):
        loader = FileSystemLoader("templates")
        environment = Environment(loader=loader)
        template = environment.get_template("extraction-job.yaml")
        out_stream = template.stream(
            job_name=job_name,
            video_bucket=bucket,
            video_file_path=video,
        )
        out_stream.dump(output_path)

    def build(self):
        folder = pathlib.Path(self.name)
        folder.mkdir()
        manifest_path = str(folder / 'manifest.yaml')
        self.create_extraction_manifest(manifest_path, self.name, self.video_bucket, self.video_path)
        return manifest_path
