pipeline {
    agent any

    environment {
        BRANCH = 'master'
    }

    parameters {
        string(name: 'NEW_MESSAGE', defaultValue: 'Hello World from Kubernetes!', description: 'Enter the new message to display')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Input Message') {
            steps {
                script {
                    echo "New message will be: ${params.NEW_MESSAGE}"
                }
            }
        }

        stage('Edit ConfigMap') {
            steps {
                script {
                    // Read the configmap file
                    def content = readFile('k8s/configmap.yaml')
                    
                    // Replace the HELLO_MESSAGE value with user input
                    def updatedContent = content.replaceAll('HELLO_MESSAGE: ".*"', "HELLO_MESSAGE: \"${params.NEW_MESSAGE}\"")
                    
                    // Write the updated content back
                    writeFile file: 'k8s/configmap.yaml', text: updatedContent
                }
            }
        }

        stage('Verify Changes') {
            steps {
                sh 'cat k8s/configmap.yaml'
            }
        }

        stage('Push Changes') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'b448d28b-3cb8-4fb4-bea8-bc0326945a2c', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_PASS')]) {
                    sh '''
                        git config user.email "jenkins@example.com"
                        git config user.name "Jenkins"
                        git add k8s/configmap.yaml
                        git commit -m "Updated HELLO_MESSAGE to: ${NEW_MESSAGE}" || echo "No changes to commit"
                        git push https://${GIT_USER}:${GIT_PASS}@github.com/KoniPN/pscp.git HEAD:${BRANCH}
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "Message successfully updated to: ${params.NEW_MESSAGE}"
        }
        failure {
            echo 'Failed to update message'
        }
    }
}
