pipeline {
    agent any

    environment {
        SEEKER_URL = 'http://192.168.12.190:8082'
        DOCKER_REGISTRY = 'kienngo22022002'
        DOCKER_CRED_ID = 'docker-hub-credentials-id'
        
        // Token Seeker
        SEEKER_ACCESS_TOKEN = credentials('seeker-agent-token')

        // Bypass SSL
        GIT_SSL_NO_VERIFY = '1'
        NODE_TLS_REJECT_UNAUTHORIZED = '0'
   }

    stages {
        stage('Checkout Code') {
            steps {
                sh 'git config --global http.sslVerify false'
                checkout scm
            }
        }

        stage('Download Seeker Agents') {
            steps {
                script {
                    echo "--- Tải các Agent Seeker ---"

                    // 1. JAVA
                    sh "rm -f src/adservice/seeker-agent.jar"
                    sh "curl -k -L '${SEEKER_URL}/rest/api/latest/installers/agents/binaries/JAVA?projectKey=microservices-demo-java&accessToken=${SEEKER_ACCESS_TOKEN}' -o src/adservice/seeker-agent.jar"
                    
                    // 2. NODE.JS
                    sh "rm -f src/paymentservice/seeker-node-agent.zip"
                    sh "curl -k -fL '${SEEKER_URL}/rest/api/latest/installers/agents/binaries/NODEJS?projectKey=microservices-demo-nodejs&accessToken=${SEEKER_ACCESS_TOKEN}' -o src/paymentservice/seeker-node-agent.zip"
                    sh "cp src/paymentservice/seeker-node-agent.zip src/currencyservice/"
                    
                    // 3. GO
                    sh "curl -k -fL '${SEEKER_URL}/rest/api/latest/installers/agents/binaries/GO?osFamily=LINUX&projectKey=microservices-demo-go&accessToken=${SEEKER_ACCESS_TOKEN}' -o /tmp/seeker-agent-linux-amd64"
                    sh "chmod +x /tmp/seeker-agent-linux-amd64"
                    sh "cp /tmp/seeker-agent-linux-amd64 src/frontend/"
                    sh "cp /tmp/seeker-agent-linux-amd64 src/checkoutservice/"
                    sh "cp /tmp/seeker-agent-linux-amd64 src/shippingservice/"
                    sh "cp /tmp/seeker-agent-linux-amd64 src/productcatalogservice/"

                    // 4. PYTHON
                    sh "curl -k -fL '${SEEKER_URL}/rest/api/latest/installers/agents/binaries/PYTHON?projectKey=microservices-demo-python&accessToken=${SEEKER_ACCESS_TOKEN}' -o /tmp/seeker-python-agent.tar.gz"
                    sh "cp /tmp/seeker-python-agent.tar.gz src/recommendationservice/"
                    sh "cp /tmp/seeker-python-agent.tar.gz src/shoppingassistantservice/"
                    sh "cp /tmp/seeker-python-agent.tar.gz src/emailservice/"
                    sh "cp /tmp/seeker-python-agent.tar.gz src/loadgenerator/"

                    // 5. .NET
		    sh "curl -k -fL '${SEEKER_URL}/rest/api/latest/installers/agents/binaries/DOTNETCORE?osFamily=LINUX&projectKey=microservices-demo-dotnet&accessToken=${SEEKER_ACCESS_TOKEN}' -o src/cartservice/src/seeker-dotnet-agent.zip"
                }
            }
        }

        stage('Build & Push: AdService (Java)') {
            steps {
                script {
                    docker.withRegistry('', "${DOCKER_CRED_ID}") {
                        dir('src/adservice') {
                            def img = docker.build("${DOCKER_REGISTRY}/adservice:iast", "--no-cache --build-arg SEEKER_ACCESS_TOKEN=${SEEKER_ACCESS_TOKEN} .")
                            img.push()
                        }
                    }
                }
            }
        }

        stage('Build & Push: PaymentService (Node.js)') {
            steps {
                script {
                    docker.withRegistry('', "${DOCKER_CRED_ID}") {
                        dir('src/paymentservice') {
                            def img = docker.build("${DOCKER_REGISTRY}/paymentservice:iast", "--no-cache --build-arg SEEKER_ACCESS_TOKEN=${SEEKER_ACCESS_TOKEN} .")
                            img.push()
                        }
                    }
                }
            }
        }

        stage('Build & Push: CheckoutService (Go)') {
            steps {
                script {
                    docker.withRegistry('', "${DOCKER_CRED_ID}") {
                        dir('src/checkoutservice') {
                            def img = docker.build("${DOCKER_REGISTRY}/checkoutservice:iast", "--no-cache --build-arg SEEKER_URL=${SEEKER_URL} --build-arg SEEKER_ACCESS_TOKEN=${SEEKER_ACCESS_TOKEN} .")
                            img.push()
                        }
                    }
                }
            }
        }

        stage('Build & Push: Frontend (Go)') {
            steps {
                script {
                    docker.withRegistry('', "${DOCKER_CRED_ID}") {
                        dir('src/frontend') {
                            def img = docker.build("${DOCKER_REGISTRY}/frontend:iast", "--no-cache --build-arg SEEKER_URL=${SEEKER_URL} --build-arg SEEKER_ACCESS_TOKEN=${SEEKER_ACCESS_TOKEN} .")
                            img.push()
                        }
                    }
                }
            }
        }

        stage('Build & Push: ShippingService (Go)') {
            steps {
                script {
                    docker.withRegistry('', "${DOCKER_CRED_ID}") {
                        dir('src/shippingservice') {
                            def img = docker.build("${DOCKER_REGISTRY}/shippingservice:iast", "--no-cache --build-arg SEEKER_URL=${SEEKER_URL} --build-arg SEEKER_ACCESS_TOKEN=${SEEKER_ACCESS_TOKEN} .")
                            img.push()
                        }
                    }
                }
            }
        }

        stage('Build & Push: RecommendationService (Python)') {
            steps {
                script {
                    docker.withRegistry('', "${DOCKER_CRED_ID}") {
                        dir('src/recommendationservice') {
                            def img = docker.build("${DOCKER_REGISTRY}/recommendationservice:iast", "--no-cache --build-arg SEEKER_ACCESS_TOKEN=${SEEKER_ACCESS_TOKEN} .")
                            img.push()
                        }
                    }
                }
            }
        }

        stage('Build & Push: ShoppingAssistant (Python)') {
            steps {
                script {
                    docker.withRegistry('', "${DOCKER_CRED_ID}") {
                        dir('src/shoppingassistantservice') {
                            def img = docker.build("${DOCKER_REGISTRY}/shoppingassistantservice:iast", "--no-cache --build-arg SEEKER_ACCESS_TOKEN=${SEEKER_ACCESS_TOKEN} .")
                            img.push()
                        }
                    }
                }
            }
        }
	stage('Build & Push: CartService (.NET)') {
            steps {
                script {
                    docker.withRegistry('', "${DOCKER_CRED_ID}") {
                        dir('src/cartservice/src') {   // <--- ĐÃ THÊM /src VÀO ĐÂY
                            def img = docker.build("${DOCKER_REGISTRY}/cartservice:iast", "--no-cache --build-arg SEEKER_ACCESS_TOKEN=${SEEKER_ACCESS_TOKEN} .")
                            img.push()
                        }
                    }
                }
            }
        }

        stage('Build & Push: CurrencyService (Node.js)') {
            steps {
                script {
                    docker.withRegistry('', "${DOCKER_CRED_ID}") {
                        dir('src/currencyservice') {
                            def img = docker.build("${DOCKER_REGISTRY}/currencyservice:iast", "--no-cache --build-arg SEEKER_ACCESS_TOKEN=${SEEKER_ACCESS_TOKEN} .")
                            img.push()
                        }
                    }
                }
            }
        }

        stage('Build & Push: EmailService (Python)') {
            steps {
                script {
                    docker.withRegistry('', "${DOCKER_CRED_ID}") {
                        dir('src/emailservice') {
                            def img = docker.build("${DOCKER_REGISTRY}/emailservice:iast", "--no-cache --build-arg SEEKER_ACCESS_TOKEN=${SEEKER_ACCESS_TOKEN} .")
                            img.push()
                        }
                    }
                }
            }
        }

        stage('Build & Push: ProductCatalogService (Go)') {
            steps {
                script {
                    docker.withRegistry('', "${DOCKER_CRED_ID}") {
                        dir('src/productcatalogservice') {
                            def img = docker.build("${DOCKER_REGISTRY}/productcatalogservice:iast", "--no-cache --build-arg SEEKER_URL=${SEEKER_URL} --build-arg SEEKER_ACCESS_TOKEN=${SEEKER_ACCESS_TOKEN} .")
                            img.push()
                        }
                    }
                }
            }
        }

        stage('Build & Push: LoadGenerator (Python)') {
            steps {
                script {
                    docker.withRegistry('', "${DOCKER_CRED_ID}") {
                        dir('src/loadgenerator') {
                            def img = docker.build("${DOCKER_REGISTRY}/loadgenerator:iast", "--no-cache --build-arg SEEKER_ACCESS_TOKEN=${SEEKER_ACCESS_TOKEN} .")
                            img.push()
                        }
                    }
                }
            }
        }
    }
    
    post {
        always {
            script {
                echo "--- Dọn dẹp Agent tạm ---"
                sh "rm -f src/adservice/seeker-agent.jar"
                sh "rm -f src/paymentservice/seeker-node-agent.zip"
                sh "rm -f src/currencyservice/seeker-node-agent.zip"
                sh "rm -f src/frontend/seeker-agent-linux-amd64"
                sh "rm -f src/checkoutservice/seeker-agent-linux-amd64"
                sh "rm -f src/shippingservice/seeker-agent-linux-amd64"
                sh "rm -f src/productcatalogservice/seeker-agent-linux-amd64"
                sh "rm -f src/recommendationservice/seeker-python-agent.tar.gz"
                sh "rm -f src/shoppingassistantservice/seeker-python-agent.tar.gz"
                sh "rm -f src/emailservice/seeker-python-agent.tar.gz"
                sh "rm -f src/loadgenerator/seeker-python-agent.tar.gz"
		sh "rm -f src/cartservice/src/seeker-dotnet-agent.zip"
                sh "rm -f /tmp/seeker-agent-linux-amd64"
                sh "rm -f /tmp/seeker-python-agent.tar.gz"
            }
        }
    }
}
