def appname = "hello-newapp"
def repo = "Daniel-Elgarisi"
def appimage = "docker.io/${repo}/${appname}"
def apptag = "${env.BUILD_NUMBER}"

podTemplate(containers: [
  containerTemplate(name: 'jnlp', image: 'jenkins/inbound-agent:latest', ttyEnabled: true),
  containerTemplate(name: 'docker', image: 'gcr.io/kaniko-project/executor:v1.23.0-debug', command: '/busybox/cat', ttyEnabled: true)
]) {
  node(POD_LABEL) {
    stage('checkout') {
      container('jnlp') {
        checkout scm
      }
    }

    stage('hello') {
      container('docker') {
        echo "Building docker image..."
        sh "echo docker push ${appimage}:${apptag}"
      }
    }
  }
}
