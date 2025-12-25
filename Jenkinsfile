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

        stage('List Files') {
            steps {
                sh 'ls -la'
                sh 'find . -name "*.py" -type f'
            }
        }

        stage('Edit app.py') {
            steps {
                script {
                    // Check if app/app.py exists (correct path based on project structure)
                    def fileExists = sh(script: 'test -f app/app.py && echo "true" || echo "false"', returnStdout: true).trim()
                    
                    if (fileExists == 'true') {
                        // Read the file
                        def content = readFile('app/app.py')
                        
                        // Edit text - replace 'old_text' with 'new_text'
                        def updatedContent = content.replace('old_text', 'new_text')
                        
                        // Write the updated content back
                        writeFile file: 'app/app.py', text: updatedContent
                    } else {
                        echo 'app/app.py not found! Creating a new one...'
                        sh 'mkdir -p app'
                        writeFile file: 'app/app.py', text: '# New app.py created by Jenkins\nprint("Hello World")\n'
                    }
                }
            }
        }

        stage('Verify Changes') {
            steps {
                sh 'cat app/app.py'
            }
        }

        stage('Push Changes') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'b448d28b-3cb8-4fb4-bea8-bc0326945a2c', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_PASS')]) {
                    sh '''
                        git config user.email "jenkins@example.com"
                        git config user.name "Jenkins"
                        git add app/app.py
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
