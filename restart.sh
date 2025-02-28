kubectl delete -f pvc-pod.yaml
kubectl delete -f pvc.yaml
kubectl create -f pvc.yaml
kubectl create -f pvc-pod.yaml

