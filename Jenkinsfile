pipeline {
    agent any

    environment {
        DOCKER_FALLBACK = 'C:\\Program Files\\Docker\\Docker\\resources\\bin\\docker.exe'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from GitHub'
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies'
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate.bat
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Unit Tests') {
            steps {
                echo 'Running unit tests'
                bat '''
                    call venv\\Scripts\\activate.bat
                    python --version
                    python -c "import pandas; import numpy; import sklearn; import streamlit; print('All imports successful')"
                '''
            }
        }
        
        stage('Train Model') {
            steps {
                echo 'Training machine learning model'
                bat '''
                    call venv\\Scripts\\activate.bat
                    if exist data\\Training.csv (
                        python train.py
                    ) else (
                        echo Data files not found, skipping training
                    )
                '''
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image'
                bat '''
                    setlocal
                    set "DOCKER_CMD=docker"
                    if exist "%DOCKER_FALLBACK%" set "DOCKER_CMD=%DOCKER_FALLBACK%"

                    call "%DOCKER_CMD%" --version
                    if errorlevel 1 (
                        echo Docker CLI not found for Jenkins. Ensure Docker Desktop is installed and available to the Jenkins service.
                        exit /b 1
                    )

                    sc query com.docker.service | find "RUNNING" >nul 2>&1
                    if errorlevel 1 (
                        echo Docker Desktop Service is stopped. Attempting to start it...
                        net start com.docker.service >nul 2>&1
                    )

                    set /a DOCKER_RETRIES=0
                    :wait_for_docker
                    call "%DOCKER_CMD%" info >nul 2>&1
                    if not errorlevel 1 goto docker_ready

                    if %DOCKER_RETRIES% GEQ 12 (
                        echo Docker daemon is not reachable from Jenkins.
                        echo Ensure Docker Desktop is running and that the Jenkins service account can access Docker.
                        exit /b 1
                    )

                    set /a DOCKER_RETRIES+=1
                    echo Waiting for Docker daemon... attempt %DOCKER_RETRIES% of 12
                    timeout /t 5 /nobreak >nul
                    goto wait_for_docker

                    :docker_ready
                    echo Docker daemon is available.

                    call "%DOCKER_CMD%" build -t disease-predictor:latest -f Dockerfile .
                '''
            }
        }
        
        stage('Test Container') {
            steps {
                echo 'Testing Docker container'
                bat '''
                    setlocal
                    set "DOCKER_CMD=docker"
                    if exist "%DOCKER_FALLBACK%" set "DOCKER_CMD=%DOCKER_FALLBACK%"

                    call "%DOCKER_CMD%" run -d --name disease-predictor-test -p 8502:8502 disease-predictor:latest
                    timeout /t 5
                    call "%DOCKER_CMD%" stop disease-predictor-test
                    call "%DOCKER_CMD%" rm disease-predictor-test
                '''
            }
        }
    }
    
    post {
        success {
            bat 'echo Build completed successfully'
        }
        failure {
            bat 'echo Build failed - check logs'
        }
    }
}
