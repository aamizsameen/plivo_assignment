pipeline {
    agent any 
    stages {
        stage('Cloning') {
            steps {
                git branch: 'main', url: 'https://github.com/aamizsameen/plivo_assignment.git'
            }
        }
        stage('Build') {
            steps {
                    sh 'sudo docker build -t webapp-deployment .'
            }
        }
        stage('Pushing to ECR') {
            steps{  
                script {
                    sh "sudo aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 973903430757.dkr.ecr.ap-south-1.amazonaws.com"
                    sh "sudo docker tag webapp-deployment:latest 973903430757.dkr.ecr.ap-south-1.amazonaws.com/aamiz-repo:latest"
                    sh "docker push 973903430757.dkr.ecr.ap-south-1.amazonaws.com/aamiz-repo:latest"
                }
            }
        }
        stage('Deploying to Kubernetes') {
          steps {
            
              sh "sudo kubectl apply -f deploy.yaml"
            
          }
        }
    }
}
