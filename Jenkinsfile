def branch = env.BRANCH_NAME
def build = env.BUILD_NUMBER
def appname = "helloworld"
def artifactory = "docker.io" 
def repo = "elevy99927" 
def appimage = "${repo}/${appname}"
def apptag = "${build}"

podTemplate(containers: [
      containerTemplate(name: 'jnlp', image: 'jenkins/inbound-agent', ttyEnabled: true),
      containerTemplate(name: 'docker', image: 'gcr.io/kaniko-project/executor:v1.23.0-debug', command: '/busybox/cat', ttyEnabled: true)
  ],
  volumes: [
     secretVolume(mountPath: '/kaniko/.docker/', secretName: 'docker-cred')
  ])  {
    node(POD_LABEL) {
        stage('checkout') {
            container('jnlp') {
                sh '/usr/bin/git config --global http.sslVerify false'
                checkout scm
            }
        }

        stage('build') {
            container('docker') {
                echo "Building docker image with Kaniko..."
                sh "/kaniko/executor --force --context=dir://${env.WORKSPACE} --destination=${appimage}:${apptag}"
            }
        }

        stage('deploy') {
            container('jnlp') {
                echo "helm install myapp"
            }
        }
    }
}
