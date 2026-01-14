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
          echo "Copying docker auth to writable config.json"
          cp /kaniko/.docker-secret/.dockerconfigjson /kaniko/.docker/config.json

          echo "Verify config.json exists:"
          ls -la /kaniko/.docker
        '''
      }
    }

    stage('push-yaml') {
    container('jnlp') {
        withCredentials([usernamePassword(credentialsId: 'github-credentials', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
            sh '''
                set -e

                git config user.email "jenkins@example.com"
                git config user.name "Jenkins"

                git remote set-url origin https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/Daniel-Elgarisi/hello-newapp.git

                if ls *.yaml *.yml 1>/dev/null 2>&1; then
                  git add *.yaml *.yml

                  if git diff --cached --quiet; then
                    echo "No YAML changes to commit"
                  else
                    git commit -m "Update YAML files - Build ${BUILD_NUMBER}"
                    git push origin HEAD:${BRANCH_NAME}
                  fi
                else
                  echo "No YAML files found, skipping push-yaml stage"
                fi
            '''
        }
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
