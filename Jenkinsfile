pipeline {
    agent any
    
    parameters {
        string(
            name: 'CUSTOM_MESSAGE',
            defaultValue: 'Hello World from DevOps Pipeline! 🚀',
            description: 'ข้อความที่จะแสดงใน H1'
        )
        string(
            name: 'VERSION',
            defaultValue: 'v1',
            description: 'Version ของ App'
        )
    }
    
    environment {
        DOCKER_HUB_USER = 'konipn'  // <-- เปลี่ยนเป็นของคุณ
        IMAGE_NAME = 'hello-world'
        IMAGE_TAG = "${params.VERSION}-${BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Update HTML Message') {
            steps {
                script {
                    // แก้ไขข้อความใน index.html
                    sh """
                        sed -i '' 's|<h1>.*</h1>|<h1>${params.CUSTOM_MESSAGE}</h1>|g' index.html
                        sed -i '' 's|<p>Version:.*</p>|<p>Version: ${params.VERSION}</p>|g' index.html
                    """
                    
                    // แสดงผลลัพธ์
                    echo "Updated index.html:"
                    sh "cat index.html"
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} ."
                sh "docker tag ${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} ${DOCKER_HUB_USER}/${IMAGE_NAME}:latest"
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh "echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin"
                    sh "docker push ${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
                    sh "docker push ${DOCKER_HUB_USER}/${IMAGE_NAME}:latest"
                }
            }
        }
        
        stage('Update Kubernetes Manifest') {
            steps {
                script {
                    // อัปเดต image tag ใน deployment.yaml
                    sh """
                        sed -i '' 's|image: .*|image: ${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}|g' deployment.yaml
                    """
                    
                    // Commit และ Push กลับไป Git (สำหรับ ArgoCD)
                    withCredentials([usernamePassword(
                        credentialsId: 'github-creds',
                        usernameVariable: 'GIT_USER',
                        passwordVariable: 'GIT_PASS'
                    )]) {
                        sh """
                            git config user.email "jenkins@example.com"
                            git config user.name "Jenkins CI"
                            git add deployment.yaml index.html
                            git commit -m "Update to ${params.CUSTOM_MESSAGE} - ${IMAGE_TAG}" || true
                            git push https://${GIT_USER}:${GIT_PASS}@github.com/KoniPN/pscp.git master
                        """
                    }
                }
            }
        }
    }
    
    post {
        success {
            echo "✅ Build สำเร็จ! Message: ${params.CUSTOM_MESSAGE}"
        }
        failure {
            echo "❌ Build ล้มเหลว!"
        }
    }
}