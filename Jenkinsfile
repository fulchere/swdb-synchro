pipeline {
    environment {
        JAVA_OPTS="-Duser.home=${JENKINS_HOME}"
        MAVEN_OPTS="${JAVA_OPTS}"
        MAVEN_CONFIG="${JENKINS_HOME}/.m2"  // docker/maven specific.
    }
  agent {
    docker {
        image 'buildtool'
        args "-e HOME=${JENKINS_HOME}"
    }
}
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
        sh 'python3 -m swdb_update'
        }
      }
    }
  }
}
