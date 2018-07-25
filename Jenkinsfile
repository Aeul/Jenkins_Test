pipeline {
  agent {
    docker {
      image 'aeul/jenkins_test'
    }

  }
  stages {
    stage('Build') {
      steps {
        sh '''cd $WORKSPACE
python3 sqlTester.py $WORKSPACE $WORKSPACE'''
      }
    }
  }
}