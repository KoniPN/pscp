pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/KoniPN/pscp.git'
        BRANCH = 'main'
    }

    stages {
        stage('Pull Repository') {
            steps {
                git branch: "${BRANCH}", url: "${REPO_URL}"
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
                sh '''
                    git config user.email "jenkins@example.com"
                    git config user.name "Jenkins"
                    git add app.py
                    git commit -m "Updated app.py via Jenkins"
                    git push origin ${BRANCH}
                '''
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
