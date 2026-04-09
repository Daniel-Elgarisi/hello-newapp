def branch = env.BRANCH_NAME
def build = env.BUILD_NUMBER
def appname = "helloworld"
def artifactory = "docker.io" 
def repo = "elevy99927" 
def appimage = "${repo}/${appname}"
def apptag = "${build}"

podTemplate(containers: [
      containerTemplate(name: 'jnlp', image: 'jenkins/inbound-agent', ttyEnabled: true),
      containerTemplate(name: 'deployer', image: 'elevy99927/k8s-deployer:latest', command: 'cat', ttyEnabled: true),
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
        // stage('calc-version') {
        //     container('deployer') {
        //         script {
        //             def currentVersion = sh(
        //                 script: """#!/bin/bash
        //                     TOKEN=\$(curl -s "https://auth.docker.io/token?service=registry.docker.io&scope=repository:${appimage}:pull" | jq -r .token)
        //                     DIGEST=\$(curl -s -H "Authorization: Bearer \$TOKEN" -H "Accept: application/vnd.docker.distribution.manifest.v2+json" "https://registry-1.docker.io/v2/${appimage}/manifests/latest" | jq -r '.config.digest // empty')
        //                     if [ -z "\$DIGEST" ]; then
        //                         echo "1"
        //                     else
        //                         CURRENT=\$(curl -s -H "Authorization: Bearer \$TOKEN" -H "Accept: application/vnd.docker.container.image.v1+json" "https://registry-1.docker.io/v2/${appimage}/blobs/\$DIGEST" | jq -r '.config.Labels.VERSION // empty')
        //                         if [ -z "\$CURRENT" ]; then
        //                             echo "1"
        //                         else
        //                             echo \$((\$CURRENT + 1))
        //                         fi
        //                     fi
        //                 """,
        //                 returnStdout: true
        //             ).trim()
        //             env.VERSION = currentVersion
        //         }
        //         echo "Next VERSION: ${env.VERSION}"
        //     }
        // }

        stage('build') {
            container('docker') {
                echo "Building docker image with Kaniko..."
                sh "/kaniko/executor --force --context=dir://${env.WORKSPACE} --destination=${appimage}:${apptag}"
            }
        }
        stage('deploy') {
            container('deployer') {
                sh """
                    apk add --no-cache git
                    GIT_TOKEN=\$(cat /var/run/secrets/github-token/token)
                    git clone https://\${GIT_TOKEN}@github.com/elevy99927/argo-demo-repo.git
                    cd argo-demo-repo
                    git checkout application

                    helm template hello-newapp ${env.WORKSPACE}/chart \
                        --set image.repository=${appimage} \
                        --set image.tag=${apptag} \
                        > app-1/k8s-qa/hello-newapp.yaml

                    git config user.email "eyal@levys.co.il"
                    git config user.name "Jenkins with Argo"
                    git add app-1/k8s-qa/hello-newapp.yaml
                    git commit -m "Deploy ${appname}:${apptag}"
                    git remote set-url origin https://\${GIT_TOKEN}@github.com/elevy99927/argo-demo-repo.git
                    git push origin application
                """
            }
        }
        stage('add-dashboard') {
            container('deployer') {
                sh """
                    GIT_TOKEN=\$(cat /var/run/secrets/github-token/token)
                    cd argo-demo-repo
                    git pull origin application

                    mkdir -p grafana-dashboards
                    cp ${env.WORKSPACE}/grafana-dashboard.json grafana-dashboards/${appname}.json

                    git add grafana-dashboards/${appname}.json
                    git commit -m "Update Grafana dashboard for ${appname}" || echo "No dashboard changes to commit"
                    git push origin application
                """
            }
        }
    }

  }