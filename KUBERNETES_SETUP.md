# KUBERNETES DEPLOYMENT GUIDE

## 📋 Prerequisites

### 1. Install kubectl
```powershell
# Using chocolatey
choco install kubernetes-cli

# Or download directly
https://kubernetes.io/docs/tasks/tools/

# Verify
kubectl version --client
```

### 2. Install Minikube (Local K8s)
```powershell
# Using chocolatey
choco install minikube

# Start minikube cluster
minikube start --driver=docker

# Check status
minikube status
```

### 3. Configure kubectl Context
```powershell
# Check current context
kubectl config current-context

# List available contexts
kubectl config get-contexts

# Switch to minikube
kubectl config use-context minikube
```

---

## 🚀 Deploy to Kubernetes

### Step 1: Update Image in Manifest

Edit `k8s-deployment.yaml`:
```yaml
image: disease-predictor:latest
# Change to your Docker Hub image:
image: your-username/disease-predictor:latest
```

### Step 2: Apply Kubernetes Manifest

```powershell
# Create namespace and deploy all resources
kubectl apply -f k8s-deployment.yaml

# Check deployment status
kubectl get all -n disease-predictor
```

### Step 3: Verify Deployment

```powershell
# Check pods
kubectl get pods -n disease-predictor

# Expected output:
# NAME                                    READY   STATUS    RESTARTS
# disease-predictor-abc123xyz-12345       1/1     Running   0
# disease-predictor-abc123xyz-67890       1/1     Running   0

# Check services
kubectl get svc -n disease-predictor

# Check deployments
kubectl get deployments -n disease-predictor
```

---

## 🌐 Access Your Application

### Option 1: Port Forward (Development)
```powershell
# Forward local port to service
kubectl port-forward -n disease-predictor svc/disease-predictor-service 8501:80

# Open browser: http://localhost:8501
```

### Option 2: Using LoadBalancer (if available)
```powershell
# Get external IP
kubectl get svc -n disease-predictor disease-predictor-service

# Access via:
# http://EXTERNAL-IP:port
```

### Option 3: Using Minikube Service
```powershell
# Get minikube service IP
minikube service -n disease-predictor disease-predictor-service --url
```

---

## 📊 Monitor Deployment

### View Pod Logs
```powershell
# Get pod name
kubectl get pods -n disease-predictor

# View logs
kubectl logs -n disease-predictor POD_NAME

# View real-time logs
kubectl logs -f -n disease-predictor POD_NAME

# View logs from all pods
kubectl logs -n disease-predictor -l app=disease-predictor
```

### Describe Resources
```powershell
# Get detailed pod info
kubectl describe pod -n disease-predictor POD_NAME

# Get service details
kubectl describe svc -n disease-predictor disease-predictor-service

# Get deployment details
kubectl describe deployment -n disease-predictor disease-predictor
```

### Monitor Resource Usage
```powershell
# CPU and memory usage
kubectl top nodes
kubectl top pods -n disease-predictor

# Watch pod status
kubectl get pods -n disease-predictor -w
```

---

## 🔄 Scaling & Auto-Scaling

### Manual Scaling
```powershell
# Scale to 3 replicas
kubectl scale deployment disease-predictor -n disease-predictor --replicas=3

# Scale to 1 replica
kubectl scale deployment disease-predictor -n disease-predictor --replicas=1
```

### Auto-Scaling (Horizontal Pod Autoscaler)
```powershell
# Check HPA status (configured in manifest)
kubectl get hpa -n disease-predictor

# Describe HPA
kubectl describe hpa disease-predictor-hpa -n disease-predictor

# View HPA events
kubectl get events -n disease-predictor --sort-by='.lastTimestamp'
```

**HPA Configuration (from manifest):**
- Min replicas: 2
- Max replicas: 5
- CPU threshold: 70%
- Memory threshold: 80%

---

## 🔒 Security & Networking

### View Network Policies
```powershell
# List network policies
kubectl get networkpolicies -n disease-predictor

# Describe policy
kubectl describe networkpolicy disease-predictor-netpolicy -n disease-predictor
```

### Check RBAC
```powershell
# List service accounts
kubectl get serviceaccounts -n disease-predictor

# Check roles
kubectl get roles -n disease-predictor

# Check role bindings
kubectl get rolebindings -n disease-predictor
```

---

## 💾 Persistent Storage

### Check Persistent Volumes
```powershell
# List PVCs
kubectl get pvc -n disease-predictor

# Describe PVC
kubectl describe pvc data-pvc -n disease-predictor

# Check PV usage
kubectl get pv

# Mount data into container
kubectl exec -it -n disease-predictor POD_NAME -- ls /app/data
```

### Copy Data to/from Cluster
```powershell
# Copy local data to pod
kubectl cp data/ disease-predictor/POD_NAME:/app/data

# Copy from pod to local
kubectl cp disease-predictor/POD_NAME:/app/model.pkl ./model.pkl
```

---

## 🐛 Troubleshooting

### Pod Failed to Start
```powershell
# Check pod status
kubectl describe pod -n disease-predictor POD_NAME

# View logs for errors
kubectl logs -n disease-predictor POD_NAME

# Common issues:
# - Image not found: verify image name and registry
# - OOMKilled: increase memory limit
# - CrashLoopBackOff: check application logs
```

### Service Not Accessible
```powershell
# Check service endpoints
kubectl get endpoints -n disease-predictor

# Test connectivity
kubectl run -it --rm debug --image=alpine --restart=Never -- sh
# Inside pod:
wget -O- http://disease-predictor-service:8501
exit
```

### Storage Issues
```powershell
# Check PVC status
kubectl get pvc -n disease-predictor

# Check storage class
kubectl get storageclass

# Describe PVC events
kubectl describe pvc -n disease-predictor data-pvc
```

---

## 🚨 Common Commands Reference

```powershell
# Namespace operations
kubectl get ns
kubectl create namespace disease-predictor
kubectl delete namespace disease-predictor

# Pod operations
kubectl get pods -n disease-predictor
kubectl delete pod POD_NAME -n disease-predictor
kubectl exec -it POD_NAME -n disease-predictor -- bash

# Deployment operations
kubectl get deployments -n disease-predictor
kubectl describe deployment disease-predictor -n disease-predictor
kubectl rollout status deployment/disease-predictor -n disease-predictor
kubectl rollout restart deployment/disease-predictor -n disease-predictor

# Service operations
kubectl get svc -n disease-predictor
kubectl expose pod POD_NAME --port=8501 -n disease-predictor

# View all resources
kubectl get all -n disease-predictor

# Delete all resources
kubectl delete all --all -n disease-predictor

# Apply configuration
kubectl apply -f k8s-deployment.yaml

# Delete configuration
kubectl delete -f k8s-deployment.yaml
```

---

## 🔄 Update Deployment

### Update Image
```powershell
# Update image in deployment
kubectl set image deployment/disease-predictor \
  disease-predictor=your-username/disease-predictor:v2.0 \
  -n disease-predictor

# Check rollout
kubectl rollout status deployment/disease-predictor -n disease-predictor

# Rollback if needed
kubectl rollout undo deployment/disease-predictor -n disease-predictor
```

### Update Configuration
```powershell
# Update entire deployment from file
kubectl apply -f k8s-deployment.yaml --record

# Check rollout history
kubectl rollout history deployment/disease-predictor -n disease-predictor

# Rollback to previous version
kubectl rollout undo deployment/disease-predictor -n disease-predictor --to-revision=1
```

---

## 📈 Advanced Monitoring

### Setup Kubernetes Dashboard
```powershell
# Install dashboard
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml

# Start proxy
kubectl proxy

# Access at: http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/
```

### Metrics Server
```powershell
# Install metrics server
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Check metrics
kubectl top nodes
kubectl top pods -n disease-predictor
```

---

## ✅ Verification Checklist

- [ ] kubectl installed and configured
- [ ] Kubernetes cluster accessible
- [ ] Namespace created: disease-predictor
- [ ] Pods running: 2+ replicas
- [ ] Service accessible: port 8501
- [ ] HPA configured and working
- [ ] Logs available and readable
- [ ] Storage mounted correctly

---

## 🎯 Complete Workflow

```
1. Local Development (Docker)
   └─> Test app locally with Docker Compose

2. CI/CD Pipeline (Jenkins)
   └─> Build → Test → Push to registry

3. Kubernetes Deployment
   └─> Deploy manifest
   └─> Monitor pods
   └─> Auto-scale on demand

4. Production
   └─> Load balance traffic
   └─> Monitor metrics
   └─> Update rolling deployments
```

---

**Need Help?**
- [Kubernetes Official Docs](https://kubernetes.io/docs/)
- [Minikube Documentation](https://minikube.sigs.k8s.io/)
- [kubectl Cheatsheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
