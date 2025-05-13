import pathlib

from jinja2 import (
    Environment,
    FileSystemLoader,
)


class VideoExtractorJobBuilder:
    def __init__(self, video_name, kubernetes_client):
        self.video_name = video_name
        self.id = abs(hash(video_name))
        self.name = f"reconstruction-{self.id}"
        self.kubernetes_client = kubernetes_client

    # TODO: extract this into a class to avoid recreating the environment
    def create_extraction_manifest(self, output_path: str, job_name: str, video: str):
        loader = FileSystemLoader("templates")
        environment = Environment(loader=loader)
        template = environment.get_template("extraction-job.yaml")
        out_stream = template.stream(job_name=job_name, video_file_name=video)
        out_stream.dump(output_path)

    def build(self):
        folder = pathlib.Path(self.name)
        folder.mkdir()
        manifest_path = str(folder / 'manifest.yaml')
        self.create_extraction_manifest(manifest_path, self.name, self.video_name)
        return manifest_path
