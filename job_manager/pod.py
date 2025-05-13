from typing import Iterator
from event_stream import EventStream
from kubernetes_client import KubernetesClient


class Pod:
    def __init__(self, client: KubernetesClient, event_stream: EventStream, name: str):
        self.client = client
        self.event_stream = event_stream
        self.name = name

        self.event_stream.add_event_listener_for(self.name, self.event_handler)

    def event_handler(self, event):
        print(event['reason'], event['message'])
        if event['reason'] == 'Started':
            for line in self.get_logs(True):
                print(line)

    def get_logs(self, follow: bool) -> Iterator[str]:
        logs = self.client.get_logs(self.name, follow)
        for line in logs:
            yield line

        # TODO send info back to the parent job when the logs run out?
