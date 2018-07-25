pipeline {
  agent {
    node {
      customWorkspace "ws\\${JOB_NAME.replace("%2F", "_")}"
      label 'agent'
    }
  }
  stages {
    stage('Build') {
      steps {
        sh '''cd ${customWorkspace}
python3 sqlTester.sql ${customWorkspace} ${customWorkspace}'''
      }
    }
  }
}
