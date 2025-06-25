pipeline {
    agent any

    environment {
        ENV_FILE = credentials('my-env-file')
    }

    stages {
        stage('Docker Test') {
            steps {
                withCredentials([file(credentialsId: 'my-env-file', variable: 'ENV_FILE_PATH')]) {
                    sh 'docker build -t fastapi-app .'
                    sh 'docker run -it --rm --env-file $ENV_FILE_PATH -p 8000:80 fastapi-app'
                }
            }
        }
    }
}
