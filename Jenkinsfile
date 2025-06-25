pipeline {
    agent any

    environment {
        IMAGE_NAME = 'fastapi-app'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Run Container (Test)') {
            steps {
                withCredentials([file(credentialsId: 'my-env-file', variable: 'ENV_FILE_PATH')]) {
                    timeout(time: 1, unit: 'MINUTES') {
                        sh '''
                            echo "Running container with .env from secrets..."
                            docker run --rm --env-file $ENV_FILE_PATH -p 8000:80 $IMAGE_NAME
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up unused Docker images...'
            sh 'docker image prune -f || true'
        }

        failure {
            echo 'Pipeline failed. Investigate the logs above.'
        }

        success {
            echo 'Pipeline completed successfully!'
        }
    }
}


// pipeline {
//     agent any

//     environment {
//         ENV_FILE = credentials('my-env-file')
//     }

//     stages {
//         stage('Docker Test') {
//             steps {
//                 withCredentials([file(credentialsId: 'my-env-file', variable: 'ENV_FILE_PATH')]) {
//                     sh 'docker build -t fastapi-app .'
//                     sh 'docker run --rm --env-file $ENV_FILE_PATH -p 8000:80 fastapi-app'
//                 }
//             }
//         }
//     }
// }

