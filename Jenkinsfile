pipeline {
  agent {
    node {
      label 'agent'
    }

  }
  stages {
    stage("Create workspace link")
    {
        def Foldername = JOB_NAME;          
        def theString = "<a href='https://jenkins.com/job/" + Foldername + "/" + BUILD_NUMBER + "/execution/node/3/ws/'>Workspace</a>";
        manager.addShortText(theString, "blue", "white", "0px", "white");
        manager.createSummary("green.gif").appendText("<h1>" + theString + "</h1>", false, false, false, "blue");
    }
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
