pipeline {
    agent any

    stages {
        stage('Docker Test') {
            steps {
                sh 'docker version'
                sh 'docker run hello-world'
            }
        }
    }
}
