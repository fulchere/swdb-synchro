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
                sh 'pip install requests'
                sh 'pip install gitpython'
                sh 'python3 -m py_compile swdb_update.py' 
            }
        }
        stage('Run') { 
            agent {
                docker {
                    image 'python:3.7-stretch' 
                }
            }
            steps {
                sh 'python3 -m swdb_update.py'

            }
        }
    }
}
