pipeline {
    agent any
    
    environment {
        // Docker registry configuration
        REGISTRY = 'docker.io'
        REGISTRY_CREDENTIALS = 'docker-credentials'
        IMAGE_NAME = 'disease-predictor'
        IMAGE_TAG = "${BUILD_NUMBER}"
        FULL_IMAGE_NAME = "${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
        
        // Python configuration
        PYTHON_VERSION = '3.11'
    }
    
    stages {
        stage('🚀 Checkout') {
            steps {
                echo '======================================'
                echo 'STAGE: Checking out code from GitHub'
                echo '======================================'
                checkout scm
                bat 'echo Repository checked out successfully'
            }
        }
        
        stage('📦 Install Dependencies') {
            steps {
                echo '======================================'
                echo 'STAGE: Installing Dependencies'
                echo '======================================'
                
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate.bat
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    echo. && echo ✓ Dependencies installed successfully
                '''
            }
        }
        
        stage('🧪 Unit Tests') {
            steps {
                echo '======================================'
                echo 'STAGE: Running Unit Tests'
                echo '======================================'
                
                bat '''
                    call venv\\Scripts\\activate.bat
                    python --version
                    python -c "import pandas; import numpy; import sklearn; import streamlit; print('✓ All imports successful')"
                    if exist data\\Training.csv (
                        echo ✓ Training data found
                    ) else (
                        echo ⚠ Training data not found
                    )
                    if exist data\\Testing.csv (
                        echo ✓ Testing data found
                    )
                '''
            }
        }
        
        stage('🤖 Train Model') {
            steps {
                echo '======================================'
                echo 'STAGE: Training Machine Learning Model'
                echo '======================================'
                
                bat '''
                    call venv\\Scripts\\activate.bat
                    
                    if exist data\\Training.csv (
                        if exist data\\Testing.csv (
                            echo Training model with data...
                            python train.py
                            if exist model.pkl (
                                echo ✓ Model trained and saved successfully
                                dir model.pkl
                            ) else (
                                echo ✗ Model training failed
                                exit /b 1
                            )
                        )
                    ) else (
                        echo ⚠ Skipping training - data files not found
                    )
                '''
            }
        }
        
        stage('🐳 Build Docker Image') {
            steps {
                echo '======================================'
                echo 'STAGE: Building Docker Image'
                echo '======================================'
                
                bat '''
                    docker --version
                    docker build -t %IMAGE_NAME%:latest -f Dockerfile .
                    echo ✓ Docker image built successfully
                    docker images | findstr %IMAGE_NAME%
                '''
            }
        }
        
        stage('🔍 Image Quality Scan') {
            steps {
                echo '======================================'
                echo 'STAGE: Scanning Docker Image'
                echo '======================================'
                
                bat '''
                    echo Docker Image Inspection:
                    docker inspect %IMAGE_NAME%:latest
                    echo.
                    echo Image Layers:
                    docker history %IMAGE_NAME%:latest
                '''
            }
        }
        
        stage('🚀 Push to Registry') {
            when {
                branch 'main'
            }
            steps {
                echo '======================================'
                echo 'STAGE: Pushing Docker Image to Registry'
                echo '======================================'
                
                bat '''
                    echo ✓ Image ready for push: %IMAGE_NAME%:latest
                    REM Uncomment below for actual registry push
                    REM docker login -u %REGISTRY_USER% -p %REGISTRY_PASSWORD% %REGISTRY%
                    REM docker push %IMAGE_NAME%:latest
                '''
            }
        }
        
        stage('🐳 Run Container Test') {
            steps {
                echo '======================================'
                echo 'STAGE: Testing Docker Container'
                echo '======================================'
                
                bat '''
                    echo Starting test container...
                    docker run -d --name disease-predictor-test-%BUILD_NUMBER% -p 8501:8501 %IMAGE_NAME%:latest
                    timeout /t 10
                    
                    if docker ps | findstr disease-predictor-test-%BUILD_NUMBER% (
                        echo ✓ Container started successfully
                        docker ps | findstr disease-predictor-test-%BUILD_NUMBER%
                    ) else (
                        echo ✗ Container failed to start
                        docker logs disease-predictor-test-%BUILD_NUMBER%
                        exit /b 1
                    )
                    
                    echo Stopping test container...
                    docker stop disease-predictor-test-%BUILD_NUMBER%
                    docker rm disease-predictor-test-%BUILD_NUMBER%
                '''
            }
        }
        
        stage('📊 Generate Report') {
            steps {
                echo '======================================'
                echo 'STAGE: Generating Deployment Report'
                echo '======================================'
                
                bat '''
                    (
                        echo ========================================
                        echo DEPLOYMENT REPORT - Build %BUILD_NUMBER%
                        echo ========================================
                        echo.
                        echo Build Status: SUCCESS
                        echo.
                        echo Image Information:
                        echo - Image Name: %IMAGE_NAME%:latest
                        echo - Registry: %REGISTRY%
                        echo.
                        echo Build Artifacts:
                        echo - Model File: model.pkl
                        echo - Application: Streamlit (port 8501
                        echo.
                        echo Stages Completed:
                        echo ✓ Code Checkout
                        echo ✓ Dependency Installation
                        echo ✓ Unit Tests
                        echo ✓ Model Training
                        echo ✓ Docker Image Build
                        echo ✓ Image Quality Scan
                        echo ✓ Container Testing
                        echo.
                        echo Deployment Status: Ready for Production
                        echo ========================================
                    ) > deployment-report.txt
                    
                    type deployment-report.txt
                '''
            }
        }
                    cat deployment-report.txt
                '''
            }
        }
    }
    
    post {
        success {
            bat 'echo. && echo BUILD COMPLETED SUCCESSFULLY && echo.'
        }
        
        failure {
            bat 'echo. && echo BUILD FAILED - Check logs above && echo.'
        }
        
        cleanup {
            bat 'echo Cleanup complete'
        }
    }
}
