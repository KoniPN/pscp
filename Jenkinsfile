pipeline {
    agent {
        kubernetes {
            // ใช้ template default ที่มี git ก็พอครับ ไม่ต้องใช้ docker
            yaml '''
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: jnlp
    image: jenkins/inbound-agent:latest
    tty: true
'''
        }
    }
    environment {
        // อย่าลืมสร้าง Credential ID: 'git-creds' ใน Jenkins ก่อนนะครับ
        GIT_CREDS = credentials('git-creds') 
        REPO_URL = 'https://github.com/KoniPN/pscp.git'
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: "${REPO_URL}", credentialsId: 'git-creds'
            }
        }
        
        stage('Modify Message') {
            steps {
                script {
                    // สร้างข้อความใหม่ตามเวลา
                    def newMsg = "Hello World - Build #${env.BUILD_NUMBER}"
                    
                    // ใช้ sed แก้ไขไฟล์ deployment.yaml 
                    // (สมมติว่าใน yaml คุณมีคำว่า "Hello World..." อยู่ใน ConfigMap หรือ Env)
                    sh """
                    sed -i 's/return ".*"/return "${newMsg}"/' k8s/deployment.yaml || true
                    # หรือถ้าแก้ใน ConfigMap ให้ปรับ regex ให้ตรงกับไฟล์ของคุณ
                    """
                    echo "Updated message to: ${newMsg}"
                }
            }
        }
        
        stage('Commit & Push (GitOps)') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'git-creds', passwordVariable: 'GIT_PASSWORD', usernameVariable: 'GIT_USERNAME')]) {
                    sh '''
                    git config user.email "jenkins@minikube.local"
                    git config user.name "Jenkins Bot"
                    
                    # เช็คก่อนว่ามีการเปลี่ยนแปลงไหม
                    if [ -n "$(git status --porcelain)" ]; then
                        git add .
                        git commit -m "Jenkins updated message to Build #${BUILD_NUMBER}"
                        git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/KoniPN/pscp.git master
                    else
                        echo "No changes to commit"
                    fi
                    '''
                }
            }
        }
    }
}