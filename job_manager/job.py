from collections import defaultdict
from typing import Callable
from event_stream import EventStream
from kubernetes_client import KubernetesClient
from pod import Pod

import re


class Job:
    def __init__(self, client: KubernetesClient, event_stream: EventStream, name: str):
        self.client = client
        self.name = name
        self.event_stream = event_stream
        self.pods = []

        self.event_stream.add_event_listener_for(self.name, self.event_listener)

    def event_listener(self, event):
        reason = event['reason']
        print(reason, event['message'])
        if reason == 'SuccessfulCreate':
            match = re.match('Created pod: (.*)', event['message'])
            pod_name = match.groups()[0]
            pod = Pod(self.client, self.event_stream, pod_name)
            self.pods.append(pod)

    def delete(self):
        pass
