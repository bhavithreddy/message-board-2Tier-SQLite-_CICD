pipeline{
    agent any
    stages{
        stage('Clone repo'){
            steps{
                git branch: 'main', url: 'https://github.com/bhavithreddy/message-board-2Tier-SQLite-_CICD.git'
            }
        }
        stage('Build image'){
            steps{
                sh 'docker build -t message-board .'
            }
        }
        stage('Deploy with docker compose'){
            steps{
                // existing container if they are running
                sh 'docker compose down || true'
                // start app, rebuilding flask image
                sh 'docker compose up -d --build'
            }
        }
    }
}