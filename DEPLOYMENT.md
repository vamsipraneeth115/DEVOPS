# Deployment Guide for Disease Prediction System

## 📋 Table of Contents
1. [Local Deployment](#local-deployment)
2. [Docker Deployment](#docker-deployment)
3. [Kubernetes Deployment](#kubernetes-deployment)
4. [Jenkins CI/CD Setup](#jenkins-cicd-setup)
5. [GitHub Integration](#github-integration)
6. [Monitoring & Troubleshooting](#monitoring--troubleshooting)

---

## Local Deployment

### Prerequisites
- Python 3.11+
- pip / virtualenv
- 4GB RAM minimum
- 2GB disk space

### Step-by-Step Setup

#### 1. Clone Repository
```bash
git clone https://github.com/your-username/disease-predictor.git
cd disease-predictor
```

#### 2. Run Setup Script
**On Linux/macOS:**
```bash
chmod +x setup.sh
./setup.sh
```

**On Windows:**
```bash
setup.bat
```

#### 3. Copy Data Files
```bash
cp /path/to/Training.csv data/
cp /path/to/Testing.csv data/
```

#### 4. Train Model
```bash
source venv/bin/activate  # Windows: venv\Scripts\activate
python train.py
```

Expected output: `model.pkl` file created

#### 5. Run Application
```bash
streamlit run app.py
```

Access at: `http://localhost:8501`

---

## Docker Deployment

### Build & Run Container

#### Build Image
```bash
# Build with default tag
docker build -t disease-predictor:latest .

# Build specific version
docker build -t disease-predictor:v1.0 .

# Build with build arguments
docker build \
  --build-arg PYTHON_VERSION=3.11 \
  -t disease-predictor:prod .
```

#### Run Container
**Single Container:**
```bash
docker run -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/model.pkl:/app/model.pkl \
  --name disease-predictor \
  disease-predictor:latest
```

**Windows:**
```cmd
docker run -p 8501:8501 ^
  -v %CD%\data:/app/data ^
  -v %CD%\model.pkl:/app/model.pkl ^
  --name disease-predictor ^
  disease-predictor:latest
```

#### Docker Compose Deployment
```bash
# Start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f disease-predictor

# Stop services
docker-compose down
```

#### Container Management
```bash
# List running containers
docker ps

# View logs
docker logs disease-predictor

# Execute command in container
docker exec disease-predictor ls -la /app

# Stop container
docker stop disease-predictor

# Remove container
docker rm disease-predictor
```

### Image Optimization
```bash
# Tag image for registry
docker tag disease-predictor:latest myregistry.io/disease-predictor:v1.0

# Push to registry
docker push myregistry.io/disease-predictor:v1.0

# Check image size
docker images | grep disease-predictor

# View image layers
docker history disease-predictor:latest
```

---

## Kubernetes Deployment

### Prerequisites
- Kubernetes cluster (v1.20+)
- kubectl configured
- Docker image in accessible registry

### Deploy to Kubernetes

#### 1. Update Image in Manifest
Edit `k8s-deployment.yaml`:
```yaml
image: your-registry.io/disease-predictor:v1.0
imagePullPolicy: Always
```

#### 2. Create Namespace and Deploy
```bash
# Apply complete manifest
kubectl apply -f k8s-deployment.yaml

# Check deployment status
kubectl get deployments -n disease-predictor
kubectl get pods -n disease-predictor
kubectl get svc -n disease-predictor

# View pod details
kubectl describe pod -n disease-predictor <pod-name>
```

#### 3. Verify Deployment
```bash
# Check pod status
kubectl get pods -n disease-predictor -w

# View logs
kubectl logs -n disease-predictor -l app=disease-predictor --tail=100

# Check service endpoints
kubectl get endpoints -n disease-predictor
```

#### 4. Access Application
```bash
# Port forward (development)
kubectl port-forward -n disease-predictor svc/disease-predictor-service 8501:80

# Or use external IP (if LoadBalancer available)
kubectl get svc -n disease-predictor disease-predictor-service
```

### Kubernetes Scaling
```bash
# Manual scaling
kubectl scale deployment disease-predictor -n disease-predictor --replicas=5

# Check HPA status
kubectl get hpa -n disease-predictor
kubectl describe hpa disease-predictor-hpa -n disease-predictor

# View resource metrics
kubectl top nodes
kubectl top pods -n disease-predictor
```

### Manage Persistent Data
```bash
# Check PVCs
kubectl get pvc -n disease-predictor

# Describe PVC
kubectl describe pvc data-pvc -n disease-predictor

# Copy data to cluster
kubectl cp data/ disease-predictor/<pod-name>:/app/data

# Copy data from cluster
kubectl cp disease-predictor/<pod-name>:/app/model.pkl ./model.pkl
```

### Delete Deployment
```bash
# Delete specific deployment
kubectl delete deployment disease-predictor -n disease-predictor

# Delete entire namespace
kubectl delete namespace disease-predictor

# Delete resources from manifest
kubectl delete -f k8s-deployment.yaml
```

---

## Jenkins CI/CD Setup

### Prerequisites
- Jenkins server installed and running
- Docker installed on Jenkins agent
- GitHub account and repository
- Docker Hub account (optional)

### Configure Jenkins Pipeline

#### 1. Install Required Plugins
In Jenkins → Manage Jenkins → Manage Plugins:
- GitHub plugin
- Docker plugin
- Pipeline plugin

#### 2. Create GitHub Webhook
1. Go to GitHub repository → Settings → Webhooks
2. Add webhook:
   - Payload URL: `http://your-jenkins:8080/github-webhook/`
   - Content type: `application/json`
   - Events: Push events

#### 3. Create Jenkins Pipeline Job
```bash
# SSH into Jenkins server
ssh jenkins@jenkins-server

# Navigate to Jenkins home
cd /var/lib/jenkins

# Create pipeline job
# Or use Jenkins UI → New Item → Pipeline
```

#### 4. Configure Pipeline
In Jenkins → Job → Pipeline:
- Repository: `https://github.com/username/disease-predictor.git`
- Script Path: `Jenkinsfile`
- Build Triggers: GitHub hook trigger

#### 5. Set Credentials
Jenkins → Manage Credentials:
- Add Docker credentials (docker-credentials)
- Add GitHub credentials (github-credentials)

#### 6. Run Pipeline
```bash
# Trigger manually
curl -X POST http://jenkins:8080/job/disease-predictor/build

# Or commit to GitHub to auto-trigger
git push origin main
```

### Monitor Jenkins Pipeline
```bash
# View pipeline console output
curl http://jenkins:8080/job/disease-predictor/1/consoleText

# Check build artifacts
# Jenkins UI → Job → Build #X → Artifacts

# View Jenkins logs
docker logs jenkins-container
# Or:
tail -f /var/log/jenkins/jenkins.log
```

---

## GitHub Integration

### Repository Setup

#### 1. Initialize Git Repository
```bash
git init
git add .
git commit -m "Initial commit: Disease prediction system"
```

#### 2. Push to GitHub
```bash
git remote add origin https://github.com/username/disease-predictor.git
git branch -M main
git push -u origin main
```

#### 3. Create GitHub Actions (Optional)
Create `.github/workflows/ci.yml`:
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    - run: pip install -r requirements.txt
    - run: python train.py
    - run: docker build -t disease-predictor:latest .
```

---

## Monitoring & Troubleshooting

### Common Issues & Solutions

#### Docker Issues
```bash
# Image not found
docker pull disease-predictor:latest
docker build -t disease-predictor:latest .

# Container won't start
docker logs disease-predictor
docker inspect disease-predictor

# Port conflicts
lsof -i :8501  # macOS/Linux
netstat -ano | findstr :8501  # Windows
```

#### Kubernetes Issues
```bash
# Pod CrashLoopBackOff
kubectl logs -n disease-predictor <pod-name>
kubectl describe pod -n disease-predictor <pod-name>

# Image pull errors
kubectl describe node <node-name>
kubectl get events -n disease-predictor

# Resource issues
kubectl top nodes
kubectl top pods -n disease-predictor
```

#### Application Issues
```bash
# Model not found
# Check: data/ directory, model.pkl file

# Slow performance
# Increase resources in k8s-deployment.yaml
# Or scale up replicas

# Data not persisting
# Check PVC status
kubectl get pvc -n disease-predictor
```

### Health Checks
```bash
# Check endpoint
curl http://localhost:8501/_stcore/health

# Kubernetes health
kubectl get pod <pod-name> -n disease-predictor -o wide

# Docker health
docker inspect disease-predictor | grep -i health
```

### Logs & Debugging
```bash
# Docker logs
docker logs -f disease-predictor

# Kubernetes logs
kubectl logs -n disease-predictor <pod-name> --tail=50

# Jenkins logs
tail -f /var/log/jenkins/jenkins.log

# Application output
streamlit run app.py --logger.level=debug
```

---

## Scaling & Performance

### Docker Swarm
```bash
# Initialize Swarm
docker swarm init

# Deploy service
docker service create \
  --name disease-predictor \
  --publish 8501:8501 \
  disease-predictor:latest

# Scale service
docker service scale disease-predictor=3
```

### Load Balancing
```bash
# Using Nginx
docker run -d --name nginx-lb \
  -p 80:80 \
  -v nginx.conf:/etc/nginx/nginx.conf \
  nginx:latest
```

### Auto-scaling
Kubernetes HPA already configured in k8s-deployment.yaml:
- Min replicas: 2
- Max replicas: 5
- CPU threshold: 70%
- Memory threshold: 80%

---

## Production Checklist

- [ ] Model trained and saved
- [ ] Docker image built and tested
- [ ] Kubernetes manifests validated
- [ ] Jenkins pipeline configured
- [ ] GitHub webhooks configured
- [ ] Monitoring and logging setup
- [ ] Backup strategy implemented
- [ ] Security policies applied
- [ ] Load testing completed
- [ ] Documentation updated

---

## Support & Resources

- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [GitHub Actions](https://github.com/features/actions)

---

**Last Updated**: 2024
**Maintenance**: Regular backups and updates recommended
**Support**: Open issues on GitHub
