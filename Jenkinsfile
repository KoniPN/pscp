// Jenkinsfile สำหรับ CI Pipeline
// ใช้สำหรับ build, test และ push Docker image ไปยัง registry

pipeline {
    agent any
    
    environment {
        // ตั้งค่า Docker registry (ใช้ Minikube's Docker daemon)
        DOCKER_IMAGE = 'hello-world'
        DOCKER_TAG = "${BUILD_NUMBER}"
        // ข้อความที่จะแสดงใน Hello World (เปลี่ยนตรงนี้เพื่อ trigger CI)
        HELLO_MESSAGE = 'Hello World from Jenkins CI!'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '📥 Checking out source code...'
                checkout scm
            }
        }
        
        stage('Update Message') {
            steps {
                echo "📝 Updating hello message to: ${HELLO_MESSAGE}"
                // อัพเดทข้อความใน deployment.yaml
                sh """
                    sed -i 's|value: ".*"  # เปลี่ยนข้อความตรงนี้|value: "${HELLO_MESSAGE}"  # เปลี่ยนข้อความตรงนี้|g' k8s/deployment.yaml
                """
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                // ใช้ Minikube's Docker daemon
                sh '''
                    eval $(minikube docker-env)
                    docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                    docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                '''
            }
        }
        
        stage('Test') {
            steps {
                echo '🧪 Running tests...'
                sh '''
                    # ทดสอบว่า container รันได้
                    eval $(minikube docker-env)
                    docker run -d --name test-container -p 5001:5000 ${DOCKER_IMAGE}:${DOCKER_TAG}
                    sleep 5
                    curl -f http://localhost:5001/health || exit 1
                    docker stop test-container
                    docker rm test-container
                '''
            }
        }
        
        stage('Update Kubernetes Manifest') {
            steps {
                echo '📦 Updating Kubernetes manifest with new image tag...'
                sh """
                    sed -i 's|image: ${DOCKER_IMAGE}:.*|image: ${DOCKER_IMAGE}:${DOCKER_TAG}|g' k8s/deployment.yaml
                """
            }
        }
        
        stage('Commit Changes') {
            steps {
                echo '📤 Committing updated manifest...'
                sh '''
                    git config user.email "jenkins@example.com"
                    git config user.name "Jenkins CI"
                    git add k8s/deployment.yaml
                    git commit -m "CI: Update image to ${DOCKER_IMAGE}:${DOCKER_TAG}" || echo "No changes to commit"
                    git push origin master || echo "Push failed - check credentials"
                '''
            }
        }
    }
    
    post {
        success {
            echo '✅ Pipeline succeeded! ArgoCD will now sync the changes.'
        }
        failure {
            echo '❌ Pipeline failed! Check the logs for details.'
        }
        always {
            echo '🧹 Cleaning up...'
            sh 'docker system prune -f || true'
        }
    }
}
