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
                withCredentials([string(credentialsId: 'github-token', variable: 'GIT_TOKEN')]) {
                sh """
                    # Clone the argo repo
                    git clone https://\${GIT_TOKEN}@github.com/elevy99927/argo-demo-repo.git
                    cd argo-demo-repo
                    git checkout application

                    # Template the helm chart with the new image tag
                    helm template hello-newapp ./helm \
                        --set image.repository=${appimage} \
                        --set image.tag=${apptag} \
                        > app-1/k8s-qa/hello-newapp.yaml

                    # Push to argo repo
                    git config user.email "eyal@levys.co.il"
                    git config user.name "Jenkins with Argo"
                    git add app-1/k8s-qa/hello-newapp.yaml
                    git commit -m "Deploy ${appname}:${apptag}"
                    git push origin application
                """
        }
    }
}

    }
}
