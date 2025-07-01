from typing import Dict, Iterator, List, Optional

import subprocess
import json


class KubernetesApiError(IOError):
    def __init__(self, command: List[str], message: str):
        super().__init__()

        self.command = command
        self.message = message

    def __repr__(self):
        representation = f"{self.__class__.__name__}(command={self.command}, message='{self.message}')"
        return representation

    def __str__(self):
        string = repr(self)
        return string


class KubernetesClient:
    def run_subcommand(self, args) -> Iterator[str]:
        command = ["kubectl", *args]
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1, # buffer per-line
            universal_newlines=True,  # utf-8
        )

        for line in process.stdout:
            yield line

        process.wait()

        if process.returncode != 0:
            stderr = ''.join(process.stderr)
            raise KubernetesApiError(command, stderr)

    def run_subcommand_json(self, args: List[str]) -> Dict:
        args = ["-o", "json", *args]
        lines = self.run_subcommand(args)
        result = json.loads(''.join(lines))
        return result

    def run_subcommand_json_stream(self, args: List[str]) -> Iterator[Dict]:
        args = ["-o", "json", *args]
        lines = self.run_subcommand(args)
        object_lines = []

        for line in lines:
            object_lines.append(line)

            if line != "}\n": # HACK
                continue

            serialized_object = ''.join(object_lines)
            object = json.loads(serialized_object)
            yield object
            object_lines.clear()

    def create_job(self, manifest_path: str) -> Dict:
        job = self.run_subcommand_json(["create", "-f", manifest_path])
        return job

    def get_jobs_pods(self, job_name: str) -> List[Dict]:
        response = self.run_subcommand_json(["get", "pods", "-l", f"job-name={job_name}"])
        pods = response['items']
        return pods

    # TODO: watch=T/F should probably be two separate functions
    def get_pod(self, name: str, watch: bool) -> Iterator[Dict]:
        if not watch:
            pod = self.run_subcommand_json(["get", "pods", name])
            yield pod
            return

        state_stream = self.run_subcommand_json_stream(["get", "pods", name, "--watch"])

        for state in state_stream:
            yield state

    def get_logs(self, resource: str, follow: bool) -> Iterator[str]:
        follow_flag = ["--follow"] * follow
        lines = self.run_subcommand(["logs", *follow_flag, resource])

        for line in lines: # this could just be `yield from` but this is nice for debugging
            yield line

    def get_events(
            self,
            watch: bool,
            watch_only: bool = False,
            resource: Optional[str] = None
        ) -> Iterator[Dict]:
        watch_flag = ["--watch"] * watch
        watch_only_flag = ["--watch-only"] * watch_only
        for_flag = ["--for", resource] * (resource is not None)
        events = self.run_subcommand_json_stream(["events", *watch_flag, *watch_only_flag, *for_flag])

        for event in events:
            yield event
