import pathlib

from jinja2 import (
    Environment,
    FileSystemLoader,
)


class ManifestBuilder:
    def __init__(
            self,
            bucket_name,
            s3_folder_path,
            job_name,
            video_file_name,
            frames_archive_file_name,
            reconstruction_archive_file_name,
        ):
        self.bucket_name = bucket_name
        self.s3_folder_path = s3_folder_path
        self.job_name = job_name
        self.video_file_name = video_file_name
        self.frames_archive_file_name = frames_archive_file_name
        self.reconstruction_archive_file_name = reconstruction_archive_file_name

        self._folder = None
        self.template_environment = Environment(loader=FileSystemLoader("templates"))

    @property
    def folder(self):
        if self._folder is None:
            self._folder = pathlib.Path(self.job_name)
            self._folder.mkdir()

        return self._folder

    def create_extraction_manifest(self, output_path: str):
        template = self.template_environment.get_template("extraction-job.yaml")
        out_stream = template.stream(
            job_name=self.job_name,
            bucket_name=self.bucket_name,
            job_folder_path=self.s3_folder_path,
            video_file_name=self.video_file_name,
            frames_archive_file_name=self.frames_archive_file_name,
        )
        out_stream.dump(output_path)

    def create_reconstruction_manifest(self, output_path: str):
        template = self.template_environment.get_template("reconstruction-job.yaml")
        out_stream = template.stream(
            job_name=self.job_name,
            bucket_name=self.bucket_name,
            job_folder_path=self.s3_folder_path,
            frames_archive_file_name=self.frames_archive_file_name,
            reconstruction_archive_file_name=self.reconstruction_archive_file_name,
        )
        out_stream.dump(output_path)

    def get_extraction_manifest(self):
        manifest_path = str(self.folder / 'extraction-manifest.yaml')
        self.create_extraction_manifest(manifest_path)
        return manifest_path

    def get_reconstruction_manifest(self):
        manifest_path = str(self.folder / 'reconstruction-manifest.yaml')
        self.create_reconstruction_manifest(manifest_path)
        return manifest_path
