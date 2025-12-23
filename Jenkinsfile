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
        NAMESPACE = 'default'
        CONFIGMAP_NAME = 'hello-world-html'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Create New HTML') {
            steps {
                script {
                    // สร้าง index.html ใหม่ตาม Parameter
                    def htmlContent = """
<!DOCTYPE html>
<html>
<head>
    <title>Hello DevOps</title>
</head>
<body>
    <h1>${params.CUSTOM_MESSAGE}</h1>
    <p>Version: ${params.VERSION}</p>
    <p>Build: #${BUILD_NUMBER}</p>
    <p>Updated: ${new Date().format('yyyy-MM-dd HH:mm:ss')}</p>
</body>
</html>
"""
                    writeFile file: 'index.html', text: htmlContent
                    echo "Created new index.html:"
                    sh "cat index.html"
                }
            }
        }
        
        stage('Update ConfigMap in Kubernetes') {
            steps {
                script {
                    // อัปเดต ConfigMap โดยตรงใน Kubernetes
                    sh """
                        kubectl create configmap ${CONFIGMAP_NAME} \
                            --from-file=index.html=index.html \
                            -n ${NAMESPACE} \
                            --dry-run=client -o yaml | kubectl apply -f -
                    """
                    echo "✅ ConfigMap updated!"
                }
            }
        }
        
        stage('Restart Deployment') {
            steps {
                script {
                    // Restart Pods เพื่อให้โหลด ConfigMap ใหม่
                    sh """
                        kubectl rollout restart deployment/hello-world -n ${NAMESPACE}
                    """
                    echo "✅ Deployment restarted!"
                    
                    // รอให้ Pods พร้อม
                    sh """
                        kubectl rollout status deployment/hello-world -n ${NAMESPACE} --timeout=60s
                    """
                }
            }
        }
        
        stage('Commit to Git') {
            steps {
                script {
                    // Commit และ Push กลับไป Git (สำหรับ ArgoCD sync)
                    withCredentials([usernamePassword(
                        credentialsId: 'github-creds',
                        usernameVariable: 'GIT_USER',
                        passwordVariable: 'GIT_PASS'
                    )]) {
                        sh """
                            git config user.email "jenkins@example.com"
                            git config user.name "Jenkins CI"
                            git add index.html
                            git commit -m "Update message: ${params.CUSTOM_MESSAGE} - Build #${BUILD_NUMBER}" || true
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
            echo "🌐 เข้าดูได้ที่: http://localhost:30080"
        }
        failure {
            echo "❌ Build ล้มเหลว!"
        }
    }
}