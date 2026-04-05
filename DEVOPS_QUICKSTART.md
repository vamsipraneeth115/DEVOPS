# COMPLETE DEVOPS DEPLOYMENT - QUICK START

## 🎯 3-TIER DEPLOYMENT: Local → CI/CD → Production

---

## 🐳 TIER 1: LOCAL DOCKER DEPLOYMENT (5 minutes)

### Terminal Commands:
```powershell
# Navigate to project
cd c:\Users\chand\OneDrive\Desktop\DEVOPS\disease-predictor

# Build Docker image
docker build -t disease-predictor:latest .

# Run with Docker Compose
docker-compose up -d

# Check status
docker-compose ps

# Stop when done
docker-compose down
```

### Access:
- **URL**: http://localhost:8501
- **Docker Desktop**: Can see container in UI

### Verify:
```powershell
# Check container logs
docker-compose logs disease-predictor

# Check running containers
docker ps | findstr disease-predictor
```

---

## 🔄 TIER 2: JENKINS CI/CD PIPELINE (30 minutes setup)

### 1. Start Jenkins via Docker
```powershell
docker run -d `
  -p 8080:8080 `
  -p 50000:50000 `
  --name jenkins `
  -v C:\jenkins_home:/var/jenkins_home `
  jenkins/jenkins:latest

# Get password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

### 2. Access Jenkins
```
http://localhost:8080
→ Enter admin password
→ Install plugins
→ Create admin user
```

### 3. Create Pipeline Job
```
1. Click "New Item"
2. Name: disease-predictor
3. Select: Pipeline
4. Configure:
   - SCM: Git
   - Repository: https://github.com/YOUR_USERNAME/disease-predictor.git
   - Script path: Jenkinsfile
5. Check: "GitHub hook trigger"
6. Save
```

### 4. Setup GitHub Webhook
```
GitHub Repo → Settings → Webhooks → Add webhook
- URL: http://your-jenkins-ip:8080/github-webhook/
- Events: Push events
```

### 5. Test Pipeline
```powershell
# Make a change and push
git push origin main

# Watch Jenkins build automatically
http://localhost:8080/job/disease-predictor/
```

---

## ☸️ TIER 3: KUBERNETES DEPLOYMENT (20 minutes setup)

### 1. Install Minikube
```powershell
# Install using Chocolate
choco install minikube

# Start local cluster
minikube start --driver=docker

# Verify
kubectl cluster-info
```

### 2. Deploy to Kubernetes
```powershell
# Apply manifest
kubectl apply -f k8s-deployment.yaml

# Check deployment
kubectl get all -n disease-predictor
kubectl get pods -n disease-predictor -w
```

### 3. Access Service
```powershell
# Option A: Port forward
kubectl port-forward -n disease-predictor svc/disease-predictor-service 8501:80

# Option B: Minikube service
minikube service -n disease-predictor disease-predictor-service --url

# Access: http://localhost:8501
```

### 4. Monitor Deployment
```powershell
# Check pod status
kubectl get pods -n disease-predictor

# View logs
kubectl logs -n disease-predictor -l app=disease-predictor -f

# Check HPA (auto-scaling)
kubectl get hpa -n disease-predictor

# Monitor resources
kubectl top pods -n disease-predictor
```

### 5. Scale Application
```powershell
# Manual scale to 3 replicas
kubectl scale deployment disease-predictor -n disease-predictor --replicas=3

# View all pods
kubectl get pods -n disease-predictor
```

---

## 🔄 COMPLETE WORKFLOW EXAMPLE

### Scenario: Update Model & Deploy

**Step 1: Local Development**
```powershell
# Make changes to app.py or train.py
# Test locally
python train.py
python run_app.py
# Visit http://localhost:8501
```

**Step 2: Commit & Push**
```bash
git add .
git commit -m "Update model features"
git push origin main
```

**Step 3: Jenkins Triggers Automatically**
```
GitHub webhook triggers Jenkins
→ Pipeline runs 8 stages:
   ✓ Checkout code
   ✓ Install dependencies
   ✓ Run tests
   ✓ Train model
   ✓ Build Docker image
   ✓ Scan image
   ✓ Push to registry
   ✓ Test container
```

**Step 4: Update Kubernetes**
```powershell
# Update image in k8s-deployment.yaml
# Apply new manifest
kubectl apply -f k8s-deployment.yaml

# Rolling update starts automatically
kubectl rollout status deployment/disease-predictor -n disease-predictor
```

---

## 📊 COMPARISON: Local vs Jenkins vs Kubernetes

| Aspect | Local Docker | Jenkins | Kubernetes |
|--------|--------------|---------|-----------|
| **Setup Time** | 5 min | 30 min | 20 min |
| **Scalability** | Single | Multiple builds | Auto-scale 2-5 pods |
| **CI/CD** | Manual | Automated | Automated rollouts |
| **High Availability** | No | No | Yes (replication) |
| **Prod Ready** | No | Partial | Yes |
| **Monitoring** | Limited | Logs | Full metrics |
| **Cost** | Free | Free | $$ (Cloud k8s) |

---

## 🚀 PRODUCTION DEPLOYMENT STEPS

### Week 1: Testing
```
Local Docker → Test all features
Docker Compose → Multi-service testing
```

### Week 2: CI/CD
```
GitHub Repo ← Code commit
Jenkins → Build & test pipeline
Docker Registry → Push image
```

### Week 3: Kubernetes
```
Minikube → Test K8s deployment
Cloud K8s → Production deployment
Auto-scaling → Handle traffic
```

### Week 4: Monitoring
```
Prometheus → Metrics collection
Grafana → Dashboard creation
Alerts → Setup notifications
```

---

## 🔧 USEFUL COMMANDS REFERENCE

### Docker
```powershell
docker build -t disease-predictor:latest .
docker-compose up -d
docker ps
docker logs CONTAINER_ID
docker exec -it CONTAINER_ID bash
```

### Jenkins
```bash
# Trigger build from CLI
curl -X POST http://localhost:8080/job/disease-predictor/build

# Get build log
curl http://localhost:8080/job/disease-predictor/1/consoleText
```

### Kubernetes
```powershell
# Deploy
kubectl apply -f k8s-deployment.yaml

# Monitor
kubectl get pods -n disease-predictor -w
kubectl logs -n disease-predictor -l app=disease-predictor -f

# Scale
kubectl scale deployment disease-predictor -n disease-predictor --replicas=5

# Update
kubectl set image deployment/disease-predictor disease-predictor=new-image:tag

# Rollback
kubectl rollout undo deployment/disease-predictor
```

---

## ✅ DEPLOYMENT CHECKLIST

**Before Local Deployment:**
- [ ] Model trained (model.pkl exists)
- [ ] App runs locally (python run_app.py)
- [ ] Docker installed
- [ ] Port 8501 available

**Before Jenkins Setup:**
- [ ] GitHub repository created & updated
- [ ] Jenkins server running
- [ ] Docker Hub account created
- [ ] Jenkins plugins installed
- [ ] GitHub webhook configured

**Before Kubernetes:**
- [ ] kubectl installed
- [ ] Minikube started (local) or K8s cluster available
- [ ] k8s-deployment.yaml updated
- [ ] Docker image in registry
- [ ] All pods running

---

## 📞 QUICK HELP

### Docker Issues:
```powershell
# Port in use?
netstat -ano | findstr :8501
# Kill process and retry

# Image not found?
docker build -t disease-predictor:latest .
docker-compose up -d
```

### Jenkins Issues:
```powershell
# Pipeline not triggering?
# → Check GitHub webhook in repository settings
# → Verify webhook delivery

# Build failing?
# → Check pipeline console output
# → Verify Docker is running
# → Check repository access
```

### Kubernetes Issues:
```powershell
# Pods not starting?
kubectl describe pod POD_NAME -n disease-predictor

# Service not accessible?
kubectl port-forward -n disease-predictor svc/disease-predictor-service 8501:80

# Resource issues?
kubectl top nodes
kubectl top pods -n disease-predictor
```

---

## 🎓 LEARNING PATH

**Beginner:**
1. Run app locally (5 min)
2. Build Docker image (10 min)
3. Run Docker Compose (5 min)

**Intermediate:**
1. Setup Jenkins (30 min)
2. Configure GitHub webhook (10 min)
3. Trigger first build (5 min)

**Advanced:**
1. Deploy to Kubernetes (20 min)
2. Setup auto-scaling (10 min)
3. Monitor with Prometheus (30 min)

---

## 🎉 YOU NOW HAVE:

✅ **Local Development**
- Docker Compose setup
- Quick launch script
- Live Streamlit app

✅ **CI/CD Pipeline**
- Jenkins configuration
- Automated builds
- Image registry push

✅ **Production Ready**
- Kubernetes manifests
- Auto-scaling (2-5 pods)
- Health monitoring
- Network policies

---

## 🚀 NEXT STEPS

### Quick Start (Choose One):
```powershell
# Option 1: Keep running locally
docker-compose up -d
# URL: http://localhost:8501

# Option 2: Deploy to Kubernetes
kubectl apply -f k8s-deployment.yaml
kubectl port-forward -n disease-predictor svc/disease-predictor-service 8501:80
# URL: http://localhost:8501

# Option 3: Full CI/CD with Jenkins
# See JENKINS_SETUP.md for detailed instructions
```

### Save This to Repository:
```bash
git add .
git commit -m "Add DevOps setup: Docker, Jenkins, Kubernetes"
git push origin main
```

---

**Total Time to Production: ~1 hour**

**Congratulations! Your disease prediction system is Now:**
- ✅ Containerized (Docker)
- ✅ Automated (Jenkins)
- ✅ Scalable (Kubernetes)
- ✅ Production Ready

---

**Questions?** See:
- Local deployment: README.md
- Docker details: Dockerfile, docker-compose.yml
- Jenkins guide: JENKINS_SETUP.md
- Kubernetes guide: KUBERNETES_SETUP.md
