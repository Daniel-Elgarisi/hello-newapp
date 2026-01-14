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
    // Writable Docker config directory
    emptyDirVolume(mountPath: '/kaniko/.docker'),

    // Secret mounted elsewhere (read-only)
    secretVolume(mountPath: '/kaniko/.docker-secret', secretName: 'docker-cred')
  ]
) {
  node(POD_LABEL) {
    stage('checkout') {
      container('jnlp') {
        checkout scm
      }
    }

    stage('prepare-docker-auth') {
      container('kaniko') {
        sh '''
          echo "Secret files:"
          ls -la /kaniko/.docker-secret

          echo "Copying docker auth to writable config.json"
          cp /kaniko/.docker-secret/.dockerconfigjson /kaniko/.docker/config.json

          echo "Verify config.json exists:"
          ls -la /kaniko/.docker
          head -n 5 /kaniko/.docker/config.json
        '''
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
