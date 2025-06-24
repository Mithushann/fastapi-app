pipeline {
    agent {
        docker {
            image 'python:3.10'
            args '-u root:root'  // Optional: Run as root if needed for permissions
        }
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Mithushann/fastapi-app.git'
            }
        }

        stage('Install dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run tests') {
            steps {
                sh 'pytest tests/'
            }
        }
    }
}
