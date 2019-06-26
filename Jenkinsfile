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
        sh 'export PYTHONPATH=$WORKSPACE:$PYTHONPATH'
      }
    }
    stage('Run') {
      agent {
        docker {
          image 'python:3.7-stretch'
        }

      }
      steps {
        sh 'python3 swdb_update.py'
      }
    }
  }
}
