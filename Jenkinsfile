pipeline {
    agent any
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
                sh 'docker build -t fraud-detection-app:latest .'
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
