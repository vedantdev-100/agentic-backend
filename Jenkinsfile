@Library("Shared") _
pipeline {
    agent any

    stages {
        stage("Hello") {
            steps{
                script{
                    snippets()
                }
            }
        }

        stage("Code") {
            steps {
                script{
                    clone("https://github.com/vedantdev-100/agentic-backend.git","main")
                }
            }
        }

        stage("Build") {
            steps {
                script{
                    docker_build("notes-app", "latest", "vedant108")
                }
            }
        }

        stage("Push to Dcoker Hub") {
            steps {
                script{
                    docker_push("notes-app", "latest", "vedant108")
                }
            }
        }
        
         stage('Docker Check') {
            steps {
                bat '''
                    docker --version
                    docker compose version
                    docker-compose --version
                    where docker
                    where docker-compose
                '''
            }
        }

        stage("Deploy") {
            steps {
                script {
                    deployFastApi()
                }
            }
        }
    }
}
