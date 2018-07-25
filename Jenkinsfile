pipeline {
  agent {
    node {
      workspace = pwd()
      label 'agent'
    }
  }
  stages {
    stage('Build') {
      steps {
        sh '''cd ${workspace}
python3 sqlTester.sql ${workspace} ${workspace}'''
      }
    }
  }
}
