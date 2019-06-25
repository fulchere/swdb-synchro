pipeline {
    agent none 
    stages {
        stage('Build') { 
            agent {
                docker {
                    image 'python:3.7-slim-stretch' 
                }
            }
            steps {
                sh 'python -m py_compile swdb_update.py' 
            }
        }
        stage('Run') { 
            agent {
                docker {
                    image 'python:3.7-slim-stretch' 
                }
            }
            steps {
                sh 'python swdb_update.py'
            }
        }
    }
}
