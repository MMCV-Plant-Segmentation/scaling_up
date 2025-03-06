kubectl delete -f frames.yaml
kubectl delete -f reconstruction.yaml
kubectl delete -f pvc.yaml

kubectl create -f pvc.yaml
kubectl create -f frames.yaml
kubectl create -f reconstruction.yaml
