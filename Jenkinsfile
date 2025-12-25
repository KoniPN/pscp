pipeline {
    agent any

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
    }

    post {
        success {
            echo 'app.py has been successfully edited!'
        }
        failure {
            echo 'Failed to edit app.py'
        }
    }
}
