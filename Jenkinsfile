pipeline {
  agent none
  stages {
    stage('Build') {
      agent {
        docker {
          image '3.6-alpine3.8'
        }

      }
      steps {
        sh 'python3 -m py_compile swdb_update.py'
      }
    }
    stage('Run') {
      agent {
        docker {
          image '3.6-alpine3.8'
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
