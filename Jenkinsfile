def branch = env.BRANCH_NAME
def build = env.BUILD_NUMBER
def appname = "helloworld"
def artifactory = "docker.io" 
def repo = "elevy99927" 
def appimage = "${repo}/${appname}"
def apptag = "${build}"

podTemplate(containers: [
      containerTemplate(name: 'jnlp', image: 'jenkins/inbound-agent', ttyEnabled: true),
      containerTemplate(name: 'deployer', image: 'alpine/helm:latest', command: 'cat', ttyEnabled: true),
      containerTemplate(name: 'docker', image: 'gcr.io/kaniko-project/executor:v1.23.0-debug', command: '/busybox/cat', ttyEnabled: true)
  ],
  volumes: [
     secretVolume(mountPath: '/kaniko/.docker/', secretName: 'docker-cred'),
     secretVolume(mountPath: '/var/run/secrets/github-token', secretName: 'github-token')

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
            container('deployer') {
                sh """
                    # Clone the argo repo
			GIT_TOKEN=$(cat /var/run/secrets/github-token/token)
			git remote set-url origin https://${GIT_TOKEN}@github.com/elevy99927/argo-demo-repo.git
			git push origin application


                    # Template the helm chart with the new image tag
                    helm template hello-newapp ${env.WORKSPACE}/chart \
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
