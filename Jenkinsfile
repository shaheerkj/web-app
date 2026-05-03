pipeline {
    agent any
    environment {
        IMAGE_NAME = "student-registration-app"
        CONTAINER_NAME = "student-app"
        APP_PORT = "5000"
    }
    stages {
        stage('Code Linting') {
            steps {
                echo 'Running Flake8 linter...'
                sh """
                    docker run --rm \
                        -v /var/jenkins_home/workspace/pipeline-web:/app \
                        -w /app \
                        python:3.11-slim \
                        bash -c \'pip install flake8 --quiet && flake8 app.py --max-line-length=120\'
                """
                echo "Linting passed!"
            }
        }
        stage('Code Build') {
            steps {
                echo 'Building Docker image...'
                sh "docker build -t ${IMAGE_NAME}:latest /var/jenkins_home/workspace/pipeline-web/"
                echo "Docker image built successfully!"
            }
        }
        stage('Containerized Deployment') {
            steps {
                echo 'Deploying application...'
                sh "docker stop ${CONTAINER_NAME} || true"
                sh "docker rm ${CONTAINER_NAME} || true"
                sh """
                    docker run -d \
                        --name ${CONTAINER_NAME} \
                        -p ${APP_PORT}:5000 \
                        ${IMAGE_NAME}:latest
                """
                sh 'sleep 5'
                sh "docker ps | grep ${CONTAINER_NAME}"
            }
        }
        stage('Containerized Selenium Testing') {
            steps {
                echo 'Running Selenium tests...'
                sh """
                    docker run --rm \
                        --network host \
                        -v /var/jenkins_home/workspace/pipeline-web/tests:/tests \
                        python:3.11-slim \
                        bash -c \'pip install selenium --quiet && apt-get update -qq && apt-get install -y -qq chromium chromium-driver && python /tests/test_selenium.py\'
                """
            }
        }
    }
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the logs above.'
            sh "docker stop ${CONTAINER_NAME} || true"
        }
        always {
            echo 'Pipeline execution finished.'
        }
    }
}
