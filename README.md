# Disease Predictor

A complete DevOps project for predicting diseases from symptoms using machine learning, Streamlit, Docker, Jenkins, and Kubernetes with Minikube.

This project covers the full flow:

1. Prepare dataset
2. Train machine learning model
3. Run Streamlit web app
4. Build Docker image
5. Run CI/CD pipeline with Jenkins
6. Deploy the app on Kubernetes using Minikube

---

## Project Features

- Disease prediction from selected symptoms
- Machine learning model using Scikit-learn
- Streamlit web interface
- Dockerized application
- Jenkins pipeline for CI/CD
- Kubernetes deployment with 2 replicas
- Service, ConfigMap, health checks, and HPA

---

## Project Structure

```text
disease-predictor/
  data/
    Training.csv
    Testing.csv
  app.py
  train.py
  model.pkl
  requirements.txt
  Dockerfile
  Jenkinsfile
  docker-compose.yml
  k8s-deployment.local.yaml
  k8s-deployment.yaml
  KUBERNETES_DEMO_GUIDE.md
  README.md
```

---

## Requirements

- Python 3.11+
- pip
- Docker Desktop
- Jenkins
- Minikube
- kubectl

---

## Dataset

The dataset files are stored in the `data` folder:

- `data/Training.csv`
- `data/Testing.csv`

The model uses symptoms as input features and predicts the disease as the output.

---

## Local Python Setup

Go to the project folder:

```powershell
cd C:\Users\chand\OneDrive\Desktop\DEVOPS\disease-predictor
```

Create virtual environment:

```powershell
python -m venv venv
```

Activate virtual environment:

```powershell
.\venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Train the model:

```powershell
python train.py
```

Run the Streamlit app locally:

```powershell
streamlit run app.py --server.port 8502
```

Open the app:

```text
http://localhost:8502
```

---

## Docker Setup

Build Docker image:

```powershell
docker build -t disease-predictor:latest .
```

Check Docker image:

```powershell
docker images disease-predictor
```

Run Docker container:

```powershell
docker run -p 8502:8502 disease-predictor:latest
```

Open the app:

```text
http://localhost:8502
```

Check app health:

```powershell
curl http://localhost:8502/_stcore/health
```

Stop the container:

```powershell
docker ps
docker stop <container_id>
```

---

## Jenkins CI/CD Pipeline

The Jenkins pipeline is defined in `Jenkinsfile`.

Pipeline stages:

1. Checkout code from GitHub
2. Verify required dataset files
3. Install Python dependencies
4. Run import/unit checks
5. Train the model
6. Build Docker image
7. Test Docker container health

Create a Jenkins pipeline job:

1. Open Jenkins
2. Create a new Pipeline job
3. Connect the GitHub repository
4. Set pipeline script path to `Jenkinsfile`
5. Run Build Now

The pipeline builds the image:

```text
disease-predictor:latest
```

---

## Kubernetes Deployment With Minikube

Start Minikube:

```powershell
minikube start
```

Use Minikube context:

```powershell
kubectl config use-context minikube
```

Check node status:

```powershell
kubectl get nodes
```

Load Docker image into Minikube:

```powershell
minikube image load disease-predictor:latest
```

Deploy the app:

```powershell
kubectl apply -f k8s-deployment.local.yaml
```

Check rollout:

```powershell
kubectl rollout status deployment/disease-predictor -n disease-predictor
```

Check Kubernetes resources:

```powershell
kubectl get all -n disease-predictor
```

Check pods:

```powershell
kubectl get pods -n disease-predictor
```

Check service:

```powershell
kubectl get svc -n disease-predictor
```

Check HPA:

```powershell
kubectl get hpa -n disease-predictor
```

Check logs:

```powershell
kubectl logs -n disease-predictor -l app=disease-predictor --tail=50
```

Open the app through port-forward:

```powershell
kubectl port-forward -n disease-predictor svc/disease-predictor-service 8502:80
```

Open in browser:

```text
http://localhost:8502
```

Health check:

```powershell
curl http://localhost:8502/_stcore/health
```

---

## Kubernetes Resources Created

The file `k8s-deployment.local.yaml` creates:

- Namespace: `disease-predictor`
- ConfigMap: `streamlit-config`
- Deployment: `disease-predictor`
- Pods: 2 replicas
- Service: `disease-predictor-service`
- HPA: `disease-predictor-hpa`

The app runs on container port `8502`.

---

## Stop And Redeploy

Stop only browser access:

```text
Press Ctrl + C in the port-forward terminal
```

Delete Kubernetes resources:

```powershell
kubectl delete -f k8s-deployment.local.yaml
```

Deploy again:

```powershell
kubectl apply -f k8s-deployment.local.yaml
```

Restart deployment after rebuilding image:

```powershell
minikube image load disease-predictor:latest
kubectl rollout restart deployment/disease-predictor -n disease-predictor
```

---

## Demo Flow

For project demonstration, show these files:

- `app.py`
- `train.py`
- `Dockerfile`
- `Jenkinsfile`
- `k8s-deployment.local.yaml`
- `KUBERNETES_DEMO_GUIDE.md`

Short explanation:

This project trains a machine learning model using symptom data, runs the model through a Streamlit web app, packages the app with Docker, validates it through Jenkins, and deploys it to Kubernetes using Minikube.

---

## Important Note

This project is for educational purposes only. It should not be used as a replacement for professional medical advice.
