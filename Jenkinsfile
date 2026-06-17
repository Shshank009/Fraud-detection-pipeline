pipeline {
    agent any
    environment {
        AWS_DEFAULT_REGION = 'ap-south-1'
        ECR_REGISTRY = '326158158021.dkr.ecr.ap-south-1.amazonaws.com'
        ECR_REPO = 'fraud-detection-app'
        IMAGE_TAG = "latest"
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
                sh 'docker build -t ${ECR_REPO}:${IMAGE_TAG} .'
            }
        }
        stage('Push to ECR') {
            steps {
                sh '''
                    aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | \
                    docker login --username AWS --password-stdin ${ECR_REGISTRY}
                '''
                sh 'docker tag ${ECR_REPO}:${IMAGE_TAG} ${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG}'
                sh 'docker push ${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG}'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker compose down || true'
                sh 'docker compose up -d --build'
            }
        }
    }
}
