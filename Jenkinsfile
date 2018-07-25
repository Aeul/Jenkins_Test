pipeline {
  agent {
    node {
      label 'agent'
    }

  }
  stages {
    stage('Initialize') {
      steps {
        echo 'This is a pipeline for testing sql scripts'
        git(url: 'https://github.com/Aeul/Jenkins_Test.git', branch: 'master')
      }
    }
    stage('Build') {
      steps {
        sh '''cd $WORKSPACE
python3 sqlTester.sql $WORKSPACE $WORKSPACE'''
      }
    }
  }
}