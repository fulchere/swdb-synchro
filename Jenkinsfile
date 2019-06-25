pipeline {
    agent none 
    stages {
        stage('Build') { 
            agent {
                docker {
                    image 'python:3.7-stretch' 
                }
            }
            steps {
                sh 'python -m py_compile swdb_update.py' 
            }
        }
        stage('Run') { 
            agent {
                docker {
                    image 'python:3.7-stretch' 
                }
            }
            steps {
                sh 'python -m swdb_update.py'
            }
        }
    }
}
