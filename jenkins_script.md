
pipeline {
    agent any

    stages {
        stage("Code") {
            steps {
                echo "This is cloning the code"
                git url:"https://github.com/vedantdev-100/agentic-backend.git", branch: "main"
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

        <!-- stage("Deploy") {
            steps {
                echo "This is deploying the code"
                bat "docker rm -f notes-app 2>nul || exit /b 0"

                withCredentials([file(credentialsId: 'fastapi-env', variable: 'ENV_FILE')]) {
                    bat 'docker run -d -p 8000:8000 --env-file "%ENV_FILE%" --name notes-app notes-app:latest'
                }

                echo "Deployed"

            }
        } -->

        <!-- ## [Best Approach] ## Compose for deployment => Update the docker compose file for jenkins --> 
        stage("Deploy") {
            steps {
                echo "Deploying the application..."

                withCredentials([
                    file(credentialsId: 'fastapi-env', variable: 'ENV_FILE')
                ]) {
                    bat '''
                        docker compose down
                        docker compose up -d --build
                    '''
                }

                echo "Deployed successfully."
            }
        }
        <!-- ## [ok Approach] ## Compose for deployment => add temp .env to the workspace during build and then delete it --> 
        stage("Deploy") {
    steps {
        echo "Deploying the application..."

        withCredentials([
            file(credentialsId: 'fastapi-env', variable: 'ENV_FILE')
        ]) {
            try {
                bat '''
                    copy /Y "%ENV_FILE%" ".env"

                    docker compose down
                    docker compose up -d --build
                '''
            } finally {
                bat '''
                    if exist ".env" del /F /Q ".env"
                '''
            }
        }

        echo "Application deployed successfully."
    }
}

    }
}




##Working file 
pipeline {
    agent any

    stages {

        stage("Code") {
            steps {
                echo "This is cloning the code"

                git(
                    url: "https://github.com/vedantdev-100/agentic-backend.git",
                    branch: "main"
                )

                echo "This code is cloned successfully..."
            }
        }

        stage("Test") {
            steps {
                echo "This is testing the code"
            }
        }

        stage("Deploy") {
            steps {
                echo "Deploying the application..."

                withCredentials([
                    file(
                        credentialsId: 'fastapi-env',
                        variable: 'ENV_FILE'
                    )
                ]) {
                    bat '''
                        copy /Y "%ENV_FILE%" ".env"

                        docker compose down
                        docker compose up -d --build

                        if exist ".env" del /F /Q ".env"
                    '''
                }

                echo "Application deployed successfully."
            }
        }
    }
}



1. Jenkinsfile → githubPush()

Install GitHub webhook forwarding
2. gh extension install cli/gh-webhook
3. gh auth login

Start forwarding GitHub → Jenkins
http://localhost:8080 (jenkins)
gh webhook forward --repo=vedantdev-100/agentic-backend --events=push --url=http://localhost:8080/github-webhook/


4. gh webhook forward ... → keep terminal running

GitHub
   │
   │ push
   ▼
GitHub CLI
   │
   │ forward
   ▼
localhost:8080/github-webhook/
   │
   ▼
Jenkins
   │
   ▼
Pipeline



## Dummy changes