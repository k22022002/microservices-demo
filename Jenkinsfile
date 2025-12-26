pipeline {
    agent any

    environment {
        SEEKER_URL = 'http://192.168.12.190:8082'
        SEEKER_PROJECT_KEY = 'microservices-demo'
        DOCKER_REGISTRY = 'kienngo22022002'
        DOCKER_CRED_ID = 'docker-hub-credentials-id'
        
        // Cấu hình SSL
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

        stage('Download Seeker Agents (Direct Binary)') {
            steps {
                // Dùng Token để tải file trực tiếp (Bỏ qua script cài đặt trung gian)
                withCredentials([string(credentialsId: 'seeker-agent-token', variable: 'SEEKER_ACCESS_TOKEN')]) {
                    script {
                        echo "--- Downloading Agent Binaries Directly ---"

                        // ==========================================================
                        // 1. JAVA AGENT (AdService) -> Tải về seeker-agent.jar
                        // ==========================================================
                        // API: /binaries/JAVA
                        sh """
                           curl -k -fL "${SEEKER_URL}/rest/api/latest/installers/agents/binaries/JAVA?projectKey=${SEEKER_PROJECT_KEY}&accessToken=${SEEKER_ACCESS_TOKEN}" \
                           -o seeker-agent.jar
                           
                           mv seeker-agent.jar src/adservice/seeker-agent.jar
                        """

                        // ==========================================================
                        // 2. NODE.JS AGENT (PaymentService) -> Tải về seeker-node-agent.zip
                        // ==========================================================
                        // API: /binaries/NODEJS (Thay vì /scripts/NODEJS)
                        // Lỗi cũ của bạn nằm ở đây, giờ tải trực tiếp zip sẽ fix được.
                        sh """
                           curl -k -fL "${SEEKER_URL}/rest/api/latest/installers/agents/binaries/NODEJS?projectKey=${SEEKER_PROJECT_KEY}&accessToken=${SEEKER_ACCESS_TOKEN}" \
                           -o seeker-node-agent.zip
                           
                           mv seeker-node-agent.zip src/paymentservice/seeker-node-agent.zip
                        """

                        // ==========================================================
                        // 3. GO AGENT (Frontend) -> Tải về seeker-agent-linux-amd64
                        // ==========================================================
                        // API: /binaries/GO
                        sh """
                           curl -k -fL "${SEEKER_URL}/rest/api/latest/installers/agents/binaries/GO?osFamily=LINUX&projectKey=${SEEKER_PROJECT_KEY}&accessToken=${SEEKER_ACCESS_TOKEN}" \
                           -o seeker-agent-linux-amd64
                           
                           chmod +x seeker-agent-linux-amd64
                           mv seeker-agent-linux-amd64 src/frontend/seeker-agent-linux-amd64
                        """
                    }
                }
            }
        }

        // --- CÁC STAGE BUILD GIỮ NGUYÊN ---
        stage('Build & Push: Java (AdService)') {
            steps {
                script {
                    docker.withRegistry('', "${DOCKER_CRED_ID}") {
                        dir('src/adservice') {
                            def img = docker.build("${DOCKER_REGISTRY}/adservice:iast", 
                                "--build-arg SEEKER_ACCESS_TOKEN=${SEEKER_ACCESS_TOKEN} .")
                            img.push()
                        }
                    }
                }
            }
        }

        stage('Build & Push: Node.js (PaymentService)') {
            steps {
                script {
                    docker.withRegistry('', "${DOCKER_CRED_ID}") {
                        dir('src/paymentservice') {
                            def img = docker.build("${DOCKER_REGISTRY}/paymentservice:iast", 
                                "--build-arg SEEKER_ACCESS_TOKEN=${SEEKER_ACCESS_TOKEN} .")
                            img.push()
                        }
                    }
                }
            }
        }

        stage('Build & Push: Go (Frontend)') {
            steps {
                script {
                    docker.withRegistry('', "${DOCKER_CRED_ID}") {
                        dir('src/frontend') {
                            def img = docker.build("${DOCKER_REGISTRY}/frontend:iast", 
                                "--build-arg SEEKER_URL=${SEEKER_URL} --build-arg SEEKER_PROJECT=${SEEKER_PROJECT_KEY} --build-arg SEEKER_ACCESS_TOKEN=${SEEKER_ACCESS_TOKEN} .")
                            img.push()
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            echo "--- Cleaning up ---"
            sh "rm -f src/adservice/seeker-agent.jar"
            sh "rm -f src/paymentservice/seeker-node-agent.zip"
            sh "rm -f src/frontend/seeker-agent-linux-amd64"
        }
        success {
            echo "✅ Build thành công IAST images."
        }
    }
}
