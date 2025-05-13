from collections import defaultdict
from typing import Callable
from kubernetes_client import KubernetesClient


class EventStream:
    def __init__(self, client: KubernetesClient):
        self.client = client
        self.subscriptions = defaultdict(list)

    def add_event_listener_for(self, object_name: str, callback: Callable[[dict], None]):
        subscribers = self.subscriptions[object_name]
        subscribers.append(callback)

    def remove_event_listener_for(self, object_name: str, callback: Callable[[dict], None]):
        subscribers = self.subscriptions[object_name]
        subscribers.remove(callback)

    def get_events(self):
        events = self.client.get_events(True)
        for event in events:
            involved_object = event['involvedObject']['name']
            subscribers = self.subscriptions.get(involved_object, [])
            for subscriber in subscribers:
                subscriber(event)

            yield event
