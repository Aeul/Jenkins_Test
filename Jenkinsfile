pipeline {
  def workspace = env.WORKSPACE
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
        sh '''cd ${workspace}
python3 sqlTester.sql ${workspace} ${workspace}'''
      }
    }
  }
}
