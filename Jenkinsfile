pipeline {
    agent any
    
    environment {
        DOCKER_HUB_USER = 'konipn'  // <-- เปลี่ยนเป็นของคุณ
        IMAGE_NAME = 'hello-world'
        IMAGE_TAG = "v${BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/KoniPN/pscp.git'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh "echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin"
                    sh "docker push ${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }
        
        stage('Update Manifest') {
            steps {
                sh """
                    sed -i 's|image: .*|image: ${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}|' deployment.yaml
                """
                
                sh """
                    git config user.email "jenkins@example.com"
                    git config user.name "Jenkins"
                    git add deployment.yaml
                    git commit -m "Update image to ${IMAGE_TAG}"
                    git push origin main
                """
            }
        }
    }
}