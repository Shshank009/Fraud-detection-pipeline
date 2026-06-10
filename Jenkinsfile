pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Shshank009/fraud-detection-pipeline.git'
            }
        }
        stage('Test') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'python -m unittest tests/test_fraud_logic.py -v'
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
