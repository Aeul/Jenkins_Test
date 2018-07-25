pipeline {
  agent {
    node {
      def workspace = env.WORKSPACE
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
