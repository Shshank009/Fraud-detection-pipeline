pipeline {
    agent any
    environment {
        AWS_DEFAULT_REGION = 'ap-south-1'
        ECR_REGISTRY = '326158158021.dkr.ecr.ap-south-1.amazonaws.com'
        ECR_REPO = 'fraud-detection-app'
        IMAGE_TAG = "build-${BUILD_NUMBER}"
        ECR_IMAGE = '326158158021.dkr.ecr.ap-south-1.amazonaws.com/fraud-detection-app'
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Shshank009/fraud-detection-pipeline.git'
            }
        }
        stage('Install Python') {
            steps {
                sh 'sudo apt-get install -y python3 python3-pip'
            }
        }
        stage('Test') {
            steps {
                sh 'pip3 install -r requirements.txt --break-system-packages'
                sh 'python3 -m unittest tests/test_fraud_logic.py -v'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${ECR_REPO}:${IMAGE_TAG} ."
                sh "docker tag ${ECR_REPO}:${IMAGE_TAG} ${ECR_REPO}:latest"
            }
        }
        stage('Push to ECR') {
            steps {
                sh "aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}"
                sh "docker tag ${ECR_REPO}:${IMAGE_TAG} ${ECR_IMAGE}:${IMAGE_TAG}"
                sh "docker tag ${ECR_REPO}:latest ${ECR_IMAGE}:latest"
                sh "docker push ${ECR_IMAGE}:${IMAGE_TAG}"
                sh "docker push ${ECR_IMAGE}:latest"
            }
        }
        stage('Deploy from ECR') {
            steps {
                sh "aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}"
                sh 'docker compose down || true'
                sh "docker pull ${ECR_IMAGE}:latest"
                sh 'docker compose up -d'
            }
        }
        stage('Cleanup') {
            steps {
                sh "docker image prune -f"
                sh "docker rmi ${ECR_REPO}:${IMAGE_TAG} || true"
                sh "docker rmi ${ECR_IMAGE}:${IMAGE_TAG} || true"
            }
        }
    }
    post {
        success {
            echo "✅ Build ${BUILD_NUMBER} deployed successfully!"
            echo "✅ Image pushed to ECR: ${ECR_IMAGE}:build-${BUILD_NUMBER}"
        }
        failure {
            echo '❌ Pipeline failed! Check the logs above.'
        }
        always {
            echo "Pipeline finished - Build #${BUILD_NUMBER}"
        }
    }
}
