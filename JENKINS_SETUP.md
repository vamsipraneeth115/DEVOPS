# JENKINS SETUP & CI/CD PIPELINE GUIDE

## 📋 Step-by-Step Jenkins Setup

### OPTION 1: Using Docker (Recommended)

#### 1. Install Jenkins via Docker
```powershell
# Pull Jenkins image
docker pull jenkins/jenkins:latest

# Run Jenkins container
docker run -d `
  -p 8080:8080 `
  -p 50000:50000 `
  --name jenkins `
  -v C:\jenkins_home:/var/jenkins_home `
  jenkins/jenkins:latest

# Get initial admin password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

#### 2. Access Jenkins
- Open browser: `http://localhost:8080`
- Enter initial admin password from above
- Install suggested plugins
- Create admin user

---

### OPTION 2: Local Installation (Windows)

#### 1. Download Jenkins
```powershell
# Download MSI installer
https://www.jenkins.io/download/

# Run installer and follow setup
```

#### 2. Start Jenkins Service
```powershell
# Jenkins runs as service on http://localhost:8080
```

---

## 🔧 Configure Pipeline in Jenkins

### Step 1: Install Required Plugins

1. Go to **Manage Jenkins** → **Manage Plugins**
2. Install these plugins:
   - GitHub plugin
   - Docker plugin
   - Pipeline plugin
   - Email Extension Plugin

### Step 2: Create New Pipeline Job

1. **New Item** → Name: `disease-predictor`
2. Select **Pipeline**
3. Click **Create**

### Step 3: Configure Pipeline

In the job configuration page:

**Build Triggers:**
- Check: ☑ "GitHub hook trigger for GITScm polling"

**Definition:**
- Select: "Pipeline script from SCM"
- SCM: **Git**
  - Repository URL: `https://github.com/YOUR_USERNAME/disease-predictor.git`
  - Credentials: Add GitHub credentials
  - Branch: `*/main`
  - Script Path: `Jenkinsfile`

**Save** the configuration

---

## 🔌 GitHub Webhook Setup

### 1. Generate GitHub Personal Token

1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token with:
   - ✓ repo (Full control of private repositories)
   - ✓ admin:repo_hook (Full control of repository hooks)

### 2. Add Jenkins Credentials in GitHub

1. Jenkins → Manage Credentials → Add credentials
   - Kind: Username with password
   - Username: your_github_username
   - Password: your_personal_token

### 3. Configure Webhook in GitHub

1. Go to your repository → Settings → Webhooks
2. Click **Add webhook**
   - Payload URL: `http://your-jenkins-ip:8080/github-webhook/`
   - Content type: `application/json`
   - Events: Select **Just the push event**
   - Active: ☑ Yes
3. Click **Add webhook**

---

## ⚙️ Configure Docker Credentials in Jenkins

1. Jenkins → Manage Credentials → Global → Add Credentials
   - Kind: **Username with password**
   - ID: `docker-credentials`
   - Username: your_docker_username
   - Password: your_docker_password (or token)
   - Description: Docker Registry

---

## 🚀 Test CI/CD Pipeline

### Trigger Build Manually

```powershell
# In Jenkins UI: Click "Build Now" button
# Or via CLI:
curl -X POST http://localhost:8080/job/disease-predictor/build
```

### Trigger via GitHub Push

```bash
# Clone your repo
git clone https://github.com/YOUR_USERNAME/disease-predictor.git
cd disease-predictor

# Make a change
echo "# Updated" >> README.md

# Push to trigger pipeline
git add .
git commit -m "Test pipeline trigger"
git push origin main
```

### Monitor Build

1. Go to Jenkins UI
2. Click on disease-predictor job
3. Click on build number (should start automatically)
4. Click **Console Output** to see build logs

---

## 📊 Jenkins Pipeline Stages Explained

The Jenkinsfile executes 8 stages:

| Stage | Purpose | Status |
|-------|---------|--------|
| 1. Checkout | Pull code from GitHub | ✅ |
| 2. Install Dependencies | Install Python packages | ✅ |
| 3. Unit Tests | Validate syntax & imports | ✅ |
| 4. Train Model | Train Decision Tree | ✅ |
| 5. Build Docker Image | Create container image | ✅ |
| 6. Image Quality Scan | Scan for vulnerabilities | ✅ |
| 7. Push to Registry | Push to Docker Hub | ✅ |
| 8. Container Testing | Test running container | ✅ |

---

## 🔍 View Build Artifacts

After successful build:

```powershell
# Get build number (e.g., 1)
# Jenkins → disease-predictor → #1

# Access artifacts
http://localhost:8080/job/disease-predictor/1/artifact/deployment-report.txt
```

---

## 📧 Email Notifications Setup (Optional)

1. Jenkins → Manage Jenkins → Configure System
2. Scroll to **Email Notification**
   - SMTP server: smtp.gmail.com
   - SMTP port: 587
   - Use SMTP Authentication: ☑
   - Username: your_email@gmail.com
   - Password: your_app_password

3. In your Jenkins Job:
   - Add post-build action: **Email Notification**
   - Recipients: your_email@gmail.com

---

## 🐛 Troubleshooting Jenkins

| Problem | Solution |
|---------|----------|
| Pipeline not triggering | Check webhook in GitHub settings |
| Docker build fails | Ensure Docker is running: `docker ps` |
| Python module errors | Check requirements.txt in Jenkinsfile |
| GitHub authentication fails | Verify personal token in Jenkins credentials |

---

## 📝 Sample Jenkinsfile Commands

```groovy
// Build stage
sh 'docker build -t disease-predictor:${BUILD_NUMBER} .'

// Push stage
sh '''
  docker login -u ${DOCKERHUB_USER} -p ${DOCKERHUB_PASS}
  docker push disease-predictor:${BUILD_NUMBER}
'''

// Deploy stage
sh '''
  docker run -d -p 8501:8501 \
    --name disease-predictor-${BUILD_NUMBER} \
    disease-predictor:${BUILD_NUMBER}
'''
```

---

## ✅ Verification Checklist

- [ ] Jenkins installed and running
- [ ] GitHub repository created
- [ ] Docker Hub account created
- [ ] Webhooks configured
- [ ] First build triggered successfully
- [ ] Docker image pushed to registry
- [ ] Artifacts generated

---

**Next Step:** Deploy to Kubernetes!
See: [KUBERNETES_SETUP.md](KUBERNETES_SETUP.md)
