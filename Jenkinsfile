def appname = "hello-newapp"
def repo = "danielelgarisi1"
def appimage = "docker.io/${repo}/${appname}"
def apptag = "${env.BUILD_NUMBER}"

podTemplate(
  containers: [
    containerTemplate(name: 'jnlp', image: 'jenkins/inbound-agent:latest', ttyEnabled: true),
    containerTemplate(name: 'kaniko', image: 'gcr.io/kaniko-project/executor:v1.23.0-debug', command: '/busybox/cat', ttyEnabled: true)
  ],
  volumes: [
    secretVolume(mountPath: '/kaniko/.docker/config.json', secretName: 'docker-cred')
  ]
) {
  node(POD_LABEL) {
    stage('checkout') {
      container('jnlp') {
        checkout scm
      }
    }

    stage('debug-docker-auth') {
      container('kaniko') {
        sh 'ls -la /kaniko/.docker || true'
        sh 'cat /kaniko/.docker/config.json | head -n 20 || true'
      }
    }

    stage('build-and-push') {
      container('kaniko') {
        sh """
          /kaniko/executor \
            --context \$PWD \
            --dockerfile Dockerfile \
            --destination ${appimage}:${apptag}
        """
      }
    }
  }
}
