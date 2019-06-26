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

      }
      steps {withEnv(["HOME=${env.WORKSPACE}"]) {
        sh "pip install gitpython --user"
        sh "pip install requests --user"
        sh 'git remote set-url website fulchere@stash.frib.msu.edu:/var/lib/jenkins/workspace/swdb-synchro_master'
        sh 'python3 -m swdb_update'
        }
      }
    }
  }
}
