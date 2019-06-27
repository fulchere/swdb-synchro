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
        sh 'python3 -m py_compile swdb_update.py'
      }
    }
    stage('Run') {
      agent {
        docker {
          image 'python:3.7-stretch'
        }
                    wrap([$class: 'BuildUser']) {
                      echo "BUILD_USER that started this Pipeline: ${BUILD_USER}"
                    }
      }
      steps {withEnv(["HOME=${env.WORKSPACE}"]) {
        sh "pip install gitpython --user"
        sh "pip install requests --user"
        sh 'ssh-keygen'
        sh 'python3 -m swdb_update'
        }
      }
    }
  }
}
