pipeline {
    agent any
    
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
                    docker --version
                    docker build -t disease-predictor:latest -f Dockerfile .
                '''
            }
        }
        
        stage('Test Container') {
            steps {
                echo 'Testing Docker container'
                bat '''
                    docker run -d --name disease-predictor-test -p 8501:8501 disease-predictor:latest
                    timeout /t 5
                    docker stop disease-predictor-test
                    docker rm disease-predictor-test
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
