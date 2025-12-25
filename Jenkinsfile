pipeline {
    agent any

    environment {
        BRANCH = 'master'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Edit app.py') {
            steps {
                script {
                    // Read the file
                    def content = readFile('app.py')
                    
                    // Edit text - replace 'old_text' with 'new_text'
                    def updatedContent = content.replace('old_text', 'new_text')
                    
                    // Write the updated content back
                    writeFile file: 'app.py', text: updatedContent
                }
            }
        }

        stage('Verify Changes') {
            steps {
                sh 'cat app.py'
            }
        }

        stage('Push Changes') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'b448d28b-3cb8-4fb4-bea8-bc0326945a2c', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_PASS')]) {
                    sh '''
                        git config user.email "jenkins@example.com"
                        git config user.name "Jenkins"
                        git add app.py
                        git commit -m "Updated app.py via Jenkins" || echo "No changes to commit"
                        git push https://${GIT_USER}:${GIT_PASS}@github.com/KoniPN/pscp.git HEAD:${BRANCH}
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'app.py has been successfully edited and changes pushed!'
        }
        failure {
            echo 'Failed to edit app.py or push changes'
        }
    }
}
