pipeline {
    agent any

    stages {
        stage("Code") {
            steps {
                echo "This is cloning the code"

                git url: "https://github.com/vedantdev-100/agentic-backend.git",
                    branch: "main"

                echo "This code is cloned successfully..."
            }
        }

        stage("Build") {
            steps {
                echo "This is building the code"

                bat "docker build -t notes-app:latest ."
            }
        }

        stage("Test") {
            steps {
                echo "This is testing the code"
            }
        }

        stage("Deploy") {
            steps {
                echo "This is deploying the code"
                echo "Checking Docker installation..."
                bat "where docker"
                bat "docker --version"

                bat "docker rm -f notes-app 2>nul || exit /b 0"

                withCredentials([
                    file(
                        credentialsId: "fastapi-env",
                        variable: "ENV_FILE"
                    )
                ]) {
                    bat 'docker run -d -p 8000:8000 --env-file "%ENV_FILE%" --name notes-app notes-app:latest'
                }

                echo "Deployed"
            }
        }
    }
}