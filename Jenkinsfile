pipeline {
    agent any

    stages {
        stage('Docker Test') {
            steps {
                sh 'docker build -t fastapi-app .'
                sh 'docker run -it --rm --env-file .env -p 8000:80 fastapi-app'
            }
        }
    }
}
