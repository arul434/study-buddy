pipeline {
    agent any
    environment {
        REGISTRY = 'localhost:5000'
        IMAGE_NAME = 'study-buddy'
        IMAGE_TAG = "v${BUILD_NUMBER}"
        FULL_IMAGE = "${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
        NAMESPACE = 'default'
    }
    stages {
        stage('Checkout Github') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/arul434/study-buddy.git']])
            }
        }        
        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    sh "docker build -t ${FULL_IMAGE} ."
                }
            }
        }
        stage('Push Image to DockerHub') {
            steps {
                script {
                    echo 'Pushing Docker image to DockerHub...'
                    // docker.withRegistry('http://registry.hub.docker.com' , "${DOCKER_HUB_CREDENTIALS_ID}") {
                    //     dockerImage.push("${IMAGE_TAG}")
                    // }
                    sh "docker push ${FULL_IMAGE}" 
                }
            }
        }
        stage('Update Deployment YAML with New Tag') {
            steps {
                script {
                    sh """
                    sed -i 's|image: study-buddy:.*|image: study-buddy:${IMAGE_TAG}|' manifests/deployment.yaml
                    """
                }
            }
        }

        stage('Commit Updated YAML') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'github-token', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_PASS')]) {
                        sh '''
                        git config user.name "arul434"
                        git config user.email "arul.dsacoe@gmail.com"
                        git add manifests/deployment.yaml
                        git commit -m "Update image tag to ${IMAGE_TAG}" || echo "No changes to commit"
                        git push https://${GIT_USER}:${GIT_PASS}@github.com/arul434/study-buddy.git HEAD:main
                        '''
                    }
                }
            }
        }
        stage('Install Kubectl & ArgoCD CLI Setup') {
            steps {
                sh '''
                echo 'installing Kubectl & ArgoCD cli...'
                curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
                chmod +x kubectl
                mv kubectl /usr/local/bin/kubectl
                curl -sSL -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
                chmod +x /usr/local/bin/argocd
                '''
            }
        }
        stage('Apply Kubernetes & Sync App with ArgoCD') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'argo', usernameVariable: 'ARGOCD_USER', passwordVariable: 'ARGOCD_PASS')]) {
                        sh '''
                        argocd login argocd.aruljr.dev --username $ARGOCD_USER --password "$ARGOCD_PASS" --insecure --grpc-web
                        argocd app sync study
                        '''
                    }
                }
            }
        }
    }
}