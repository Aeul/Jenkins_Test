pipeline {
  agent {
    docker {
      image 'aeul/jenkins_test'
    }

  }
  stages {
    stage('Git') {
      steps {
        git(url: 'https://github.com/Aeul/Jenkins_Test.git', branch: 'master', changelog: true)
      }
    }
    stage('Run Shell') {
      steps {
        sh '''cd $WORKSPACE
python3 sqlTester.py $WORKSPACE $WORKSPACE'''
      }
    }
  }
}