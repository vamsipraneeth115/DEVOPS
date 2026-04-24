# Kubernetes Demo Guide - Disease Predictor

This guide is for demonstrating the Kubernetes deployment of the Disease Prediction System to your guide/evaluator.

The project already has:

- Machine Learning model training
- Streamlit web application
- Docker containerization
- Jenkins CI/CD pipeline
- Kubernetes deployment using a local Kind cluster

---

## 1. What We Are Demonstrating

In this demo, we show that the Dockerized Disease Predictor application is deployed and running inside Kubernetes.

Kubernetes resources created:

- Namespace: `disease-predictor`
- Deployment: `disease-predictor`
- Pods: 2 running replicas
- Service: `disease-predictor-service`
- ConfigMap: `streamlit-config`
- Horizontal Pod Autoscaler: `disease-predictor-hpa`

Application URL during demo:

```text
http://localhost:8502
```

---

## 2. Important Files To Show

Show these files during the demo:

```text
Dockerfile
Jenkinsfile
k8s-deployment.local.yaml
KUBERNETES_DEMO_GUIDE.md
```

Explain briefly:

- `Dockerfile` builds the application image.
- `Jenkinsfile` runs CI/CD steps like install, test, train model, build Docker image, and test container.
- `k8s-deployment.local.yaml` deploys the app to Kubernetes.
- `KUBERNETES_DEMO_GUIDE.md` contains the demo steps.

---

## 3. Go To Project Directory

Open PowerShell and run:

```powershell
cd C:\Users\chand\OneDrive\Desktop\DEVOPS\disease-predictor
```

Expected:

```text
You are now inside the disease-predictor project folder.
```

---

## 4. Check Kubernetes Context

Run:

```powershell
kubectl config current-context
```

Expected output:

```text
kind-disease-predictor
```

What to explain:

```text
This shows that kubectl is connected to our local Kubernetes cluster created using Kind.
```

If no context is shown, use:

```powershell
.\.tools\kind.exe get clusters
```

Expected:

```text
disease-predictor
```

Then set context:

```powershell
kubectl config use-context kind-disease-predictor
```

---

## 5. Check Kubernetes Node

Run:

```powershell
kubectl get nodes
```

Expected output example:

```text
NAME                              STATUS   ROLES           AGE   VERSION
disease-predictor-control-plane   Ready    control-plane   10m   v1.32.2
```

What to explain:

```text
This confirms that the Kubernetes cluster is running and the node is ready.
```

---

## 6. Build Docker Image

Run:

```powershell
docker build -t disease-predictor:latest .
```

Expected output near the end:

```text
naming to docker.io/library/disease-predictor:latest done
DONE
```

What to explain:

```text
This command builds the Docker image for the Streamlit disease prediction application.
The image includes the app code, dataset files, dependencies, and trained model.
```

---

## 7. Load Docker Image Into Kubernetes Cluster

Because we are using a local Kind cluster, we load the Docker image into the cluster manually.

Run:

```powershell
.\.tools\kind.exe load docker-image disease-predictor:latest --name disease-predictor
```

Expected output:

```text
Image: "disease-predictor:latest" with ID "sha256:..." not yet present on node "disease-predictor-control-plane", loading...
```

or:

```text
Image already present on all nodes.
```

What to explain:

```text
Kind runs Kubernetes inside Docker, so the image must be loaded into the Kind cluster before Kubernetes can run it.
```

---

## 8. Deploy Application To Kubernetes

Run:

```powershell
kubectl apply -f k8s-deployment.local.yaml
```

Expected output:

```text
namespace/disease-predictor created
configmap/streamlit-config created
deployment.apps/disease-predictor created
service/disease-predictor-service created
horizontalpodautoscaler.autoscaling/disease-predictor-hpa created
```

If already deployed, expected output may be:

```text
namespace/disease-predictor unchanged
configmap/streamlit-config unchanged
deployment.apps/disease-predictor unchanged
service/disease-predictor-service unchanged
horizontalpodautoscaler.autoscaling/disease-predictor-hpa unchanged
```

What to explain:

```text
This applies the Kubernetes manifest and creates all required Kubernetes resources.
```

---

## 9. Check All Kubernetes Resources

Run:

```powershell
kubectl get all -n disease-predictor
```

Expected output example:

```text
NAME                                     READY   STATUS    RESTARTS   AGE
pod/disease-predictor-7cbf74b76f-4mh6v   1/1     Running   0          2m
pod/disease-predictor-7cbf74b76f-76lvh   1/1     Running   0          2m

NAME                                TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
service/disease-predictor-service   LoadBalancer   10.96.63.174   <pending>     80:31461/TCP   2m

NAME                                READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/disease-predictor   2/2     2            2           2m

NAME                                           DESIRED   CURRENT   READY   AGE
replicaset.apps/disease-predictor-7cbf74b76f   2         2         2       2m

NAME                                                        REFERENCE                      TARGETS                                     MINPODS   MAXPODS   REPLICAS   AGE
horizontalpodautoscaler.autoscaling/disease-predictor-hpa   Deployment/disease-predictor   cpu: <unknown>/70%, memory: <unknown>/80%   2         5         2          2m
```

What to explain:

```text
The application is running in two pods.
The deployment manages the replicas.
The service exposes the application.
The HPA is configured for autoscaling.
```

Note:

```text
EXTERNAL-IP shows <pending> because this is a local Kind cluster.
For local demo access, we use kubectl port-forward.
```

---

## 10. Check Pods Separately

Run:

```powershell
kubectl get pods -n disease-predictor
```

Expected output:

```text
NAME                                 READY   STATUS    RESTARTS   AGE
disease-predictor-xxxxxxxxxx-xxxxx   1/1     Running   0          2m
disease-predictor-xxxxxxxxxx-yyyyy   1/1     Running   0          2m
```

What to explain:

```text
Both pods are running successfully.
READY 1/1 means the application container inside the pod is healthy.
```

---

## 11. Check Deployment Rollout

Run:

```powershell
kubectl rollout status deployment/disease-predictor -n disease-predictor
```

Expected output:

```text
deployment "disease-predictor" successfully rolled out
```

What to explain:

```text
This confirms that Kubernetes successfully deployed the latest application version.
```

---

## 12. Check Application Logs

Run:

```powershell
kubectl logs -n disease-predictor -l app=disease-predictor --tail=50
```

Expected output example:

```text
Collecting usage statistics. To deactivate, set browser.gatherUsageStats to false.

You can now view your Streamlit app in your browser.

URL: http://0.0.0.0:8502
```

What to explain:

```text
These are logs from the application pods.
They show that the Streamlit application has started successfully inside Kubernetes.
```

---

## 13. Access The Application

Run:

```powershell
kubectl port-forward -n disease-predictor svc/disease-predictor-service 8502:80
```

Expected output:

```text
Forwarding from 127.0.0.1:8502 -> 8502
Forwarding from [::1]:8502 -> 8502
```

Keep this terminal running.

Open browser:

```text
http://localhost:8502
```

What to explain:

```text
The app is running inside Kubernetes, and port-forward maps the Kubernetes service to localhost so we can access it in the browser.
```

---

## 14. Health Check

Open a second PowerShell terminal and run:

```powershell
curl http://localhost:8502/_stcore/health
```

Expected output:

```text
ok
```

What to explain:

```text
This health endpoint is used to verify that the Streamlit app is alive.
The Kubernetes liveness and readiness probes also use this endpoint.
```

---

## 15. Show Autoscaling Configuration

Run:

```powershell
kubectl get hpa -n disease-predictor
```

Expected output example:

```text
NAME                    REFERENCE                      TARGETS                                     MINPODS   MAXPODS   REPLICAS
disease-predictor-hpa   Deployment/disease-predictor   cpu: <unknown>/70%, memory: <unknown>/80%   2         5         2
```

What to explain:

```text
The HPA is configured to keep minimum 2 pods and scale up to 5 pods based on CPU and memory usage.
The metrics may show unknown locally if metrics-server is not installed, but the autoscaling object is configured.
```

---

## 16. Show Service Details

Run:

```powershell
kubectl get svc -n disease-predictor
```

Expected output:

```text
NAME                        TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)
disease-predictor-service   LoadBalancer   10.x.x.x        <pending>     80:xxxxx/TCP
```

What to explain:

```text
The service exposes the pods.
In local Kind Kubernetes, LoadBalancer external IP remains pending, so we use port-forward for browser access.
```

---

## 17. Explain The Kubernetes Manifest

Open:

```text
k8s-deployment.local.yaml
```

Explain each section:

```text
Namespace:
Creates a separate Kubernetes area called disease-predictor.

ConfigMap:
Stores Streamlit server configuration.

Deployment:
Runs two replicas of the disease predictor application.

Liveness Probe:
Checks if the app is alive.

Readiness Probe:
Checks if the app is ready to receive traffic.

Service:
Exposes the app inside Kubernetes.

HPA:
Configures autoscaling from 2 to 5 pods.
```

---

## 18. Final Demo Explanation Script

You can say this to your guide:

```text
First, we developed a machine learning based disease prediction system using Streamlit.
Then we containerized the application using Docker.
Jenkins is used for CI/CD, where it installs dependencies, runs tests, trains the model, builds the Docker image, and tests the container.

For Kubernetes deployment, we created a local Kubernetes cluster using Kind.
Then we loaded the Docker image into the Kind cluster and applied the Kubernetes manifest.
The manifest creates a namespace, config map, deployment, service, and horizontal pod autoscaler.

The application is running with two pod replicas for availability.
The service exposes the application, and since this is a local Kind cluster, we access it using kubectl port-forward.
Finally, we verify the application through the browser and health check endpoint.
```

---

## 19. Complete Command Sequence For Demo

Use this sequence if you want to run the whole demo from start to finish.

```powershell
cd C:\Users\chand\OneDrive\Desktop\DEVOPS\disease-predictor

kubectl config current-context

kubectl get nodes

docker build -t disease-predictor:latest .

.\.tools\kind.exe load docker-image disease-predictor:latest --name disease-predictor

kubectl apply -f k8s-deployment.local.yaml

kubectl rollout status deployment/disease-predictor -n disease-predictor

kubectl get all -n disease-predictor

kubectl logs -n disease-predictor -l app=disease-predictor --tail=50

kubectl get hpa -n disease-predictor

kubectl port-forward -n disease-predictor svc/disease-predictor-service 8502:80
```

Then open:

```text
http://localhost:8502
```

---

## 20. Cleanup Commands

Use this only after the demo if you want to remove Kubernetes resources.

Delete app resources:

```powershell
kubectl delete -f k8s-deployment.local.yaml
```

Delete the Kind cluster:

```powershell
.\.tools\kind.exe delete cluster --name disease-predictor
```

Warning:

```text
Do not run cleanup before the demo.
```

---

## 21. Troubleshooting

### Pod Not Running

Run:

```powershell
kubectl describe pod -n disease-predictor <pod-name>
kubectl logs -n disease-predictor <pod-name>
```

### Image Pull Error

Run:

```powershell
docker build -t disease-predictor:latest .
.\.tools\kind.exe load docker-image disease-predictor:latest --name disease-predictor
kubectl rollout restart deployment/disease-predictor -n disease-predictor
```

### Port Already In Use

Use another local port:

```powershell
kubectl port-forward -n disease-predictor svc/disease-predictor-service 8503:80
```

Then open:

```text
http://localhost:8503
```

### Context Not Set

Run:

```powershell
kubectl config use-context kind-disease-predictor
```

### Cluster Not Found

Run:

```powershell
.\.tools\kind.exe create cluster --name disease-predictor
```

Then repeat:

```powershell
.\.tools\kind.exe load docker-image disease-predictor:latest --name disease-predictor
kubectl apply -f k8s-deployment.local.yaml
```

