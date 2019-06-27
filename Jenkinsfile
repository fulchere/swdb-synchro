pipeline {
  agent none
  stages {
    stage('Build') {
      agent {
        docker {
          image 'python:3.6-jessie'
        }

      }
      steps {
        sh 'python3 -m py_compile swdb_update.py'
      }
    }
    stage('Run') {
      agent {
        docker {
          image 'python:3.6-jessie'
        }
      }
      steps {withEnv(["HOME=${env.WORKSPACE}"]) {
        sh "pip install gitpython --user"
        sh "pip install requests --user"
        sh 'python3 -m swdb_update'
        }
      }
    }
  }
}
