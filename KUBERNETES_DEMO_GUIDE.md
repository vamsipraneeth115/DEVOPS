# Kubernetes Demo Guide - Disease Predictor

Simple Minikube commands to deploy and show the project.

App URL: http://localhost:8502

---

## Files To Show

Docker image file:
Dockerfile

Jenkins CI/CD file:
Jenkinsfile

Kubernetes deployment file:
k8s-deployment.local.yaml

---

## Deploy On Minikube

Go to the project folder:
cd C:\Users\chand\OneDrive\Desktop\DEVOPS\disease-predictor

Start Minikube:
minikube start

Use Minikube context:
kubectl config use-context minikube

Check Kubernetes node:
kubectl get nodes

Check local Docker image:
docker images disease-predictor

Load Docker image into Minikube:
minikube image load disease-predictor:latest

Deploy the app:
kubectl apply -f k8s-deployment.local.yaml

Wait for deployment:
kubectl rollout status deployment/disease-predictor -n disease-predictor

Check all app resources:
kubectl get all -n disease-predictor

Check pods:
kubectl get pods -n disease-predictor

Check service:
kubectl get svc -n disease-predictor

Check autoscaling:
kubectl get hpa -n disease-predictor

Check app logs:
kubectl logs -n disease-predictor -l app=disease-predictor --tail=50

Open the app locally:
kubectl port-forward -n disease-predictor svc/disease-predictor-service 8502:80

Open in browser:
http://localhost:8502

Check health from another terminal:
curl http://localhost:8502/_stcore/health

---

## Stop And Show Again

Stop browser access:
Press Ctrl + C in the port-forward terminal

Delete app from Kubernetes:
kubectl delete -f k8s-deployment.local.yaml

Deploy again for demo:
kubectl apply -f k8s-deployment.local.yaml

Open app again:
kubectl port-forward -n disease-predictor svc/disease-predictor-service 8502:80

---

## If Image Is Missing

Build Docker image:
docker build -t disease-predictor:latest .

Load image into Minikube:
minikube image load disease-predictor:latest

Restart deployment:
kubectl rollout restart deployment/disease-predictor -n disease-predictor

---

## Short Demo Explanation

This is a Streamlit disease prediction app containerized using Docker.
The Docker image is loaded into Minikube.
The app is deployed using k8s-deployment.local.yaml.
Kubernetes creates pods, service, deployment, config map, and HPA.
The app is opened locally using kubectl port-forward.
