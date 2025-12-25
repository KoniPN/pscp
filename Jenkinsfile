pipeline {
    agent {
        kubernetes {
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
        REPO_URL = 'https://github.com/KoniPN/pscp.git'
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: "${REPO_URL}", credentialsId: 'b448d28b-3cb8-4fb4-bea8-bc0326945a2c'
            }
        }
        
        stage('Modify Message') {
            steps {
                script {
                    def newMsg = "Hello World - Build #${env.BUILD_NUMBER}"
                    sh """
                    sed -i 's/return ".*"/return "${newMsg}"/' k8s/deployment.yaml || true
                    """
                    echo "Updated message to: ${newMsg}"
                }
            }
        }
        
        stage('Commit & Push (GitOps)') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'b448d28b-3cb8-4fb4-bea8-bc0326945a2c', passwordVariable: 'GIT_PASSWORD', usernameVariable: 'GIT_USERNAME')]) {
                    sh '''
                    git config user.email "jenkins@minikube.local"
                    git config user.name "Jenkins Bot"
                    
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