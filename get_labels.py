import json
import subprocess


k8 = subprocess.Popen(
    ['kubectl', 'get', 'nodes', '-A', '-o', 'json'],
    stdout=subprocess.PIPE,
)
stdout, stderr = k8.communicate()
response = json.loads(stdout)

labels_set = {key for nodes in response['items'] for key in nodes['metadata']['labels'].keys()}
labels = list(labels_set)
labels.sort()

for label in labels:
    print(label)

