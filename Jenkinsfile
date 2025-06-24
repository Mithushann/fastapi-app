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
                sh ' docker build -t fastapi-app .'
                sh 'docker run -it --rm --env-file .env -p 8000:80 fastapi-app'
            }
        }

        stage('Run tests') {
            steps {
                sh 'docker run --rm fastapi-app pytest tests/'
            }
        }
    }
}
