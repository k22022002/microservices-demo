pipeline {
    agent any

    environment {
        // --- CẤU HÌNH SEEKER & DOCKER ---
        SEEKER_URL = 'http://192.168.12.190:8082'
        SEEKER_PROJECT_KEY = 'microservices-demo'
        DOCKER_REGISTRY = 'kienngo22022002'
        DOCKER_CRED_ID = 'docker-hub-credentials-id'

        // --- FIX LỖI SSL & TIME ---
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

        stage('Download Seeker Agents (Standard Guide)') {
            steps {
                // Sử dụng plugin Credentials Binding để lấy Token an toàn
                withCredentials([string(credentialsId: 'seeker-agent-token', variable: 'SEEKER_ACCESS_TOKEN')]) {
                    script {
                        echo "--- Downloading Agents via Installer Scripts ---"

                        // ==================================================================================
                        // 1. JAVA AGENT (AdService)
                        // ==================================================================================
                        echo "Downloading Java Agent..."
                        // Tải script cài đặt
                        sh """
                            curl -k -sSL -o java_installer.sh "${SEEKER_URL}/rest/api/latest/installers/agents/scripts/JAVA?osFamily=LINUX&downloadWith=curl&webServer=ALL&flavor=DEFAULT&projectKey=${SEEKER_PROJECT_KEY}&accessToken=${SEEKER_ACCESS_TOKEN}"
                            chmod +x java_installer.sh
                        """
                        // Chạy script để tải file .jar, sau đó di chuyển vào src/adservice
                        sh """
                            ./java_installer.sh --download-only
                            mv seeker-agent.jar src/adservice/seeker-agent.jar || echo "File not found or already moved"
                        """

                        // ==================================================================================
                        // 2. NODE.JS AGENT (PaymentService)
                        // ==================================================================================
                        echo "Downloading Node.js Agent..."
                        // URL dựa trên hình ảnh image_b6ec1b.png
                        sh """
                            curl -k -sSL -o node_installer.sh "${SEEKER_URL}/rest/api/latest/installers/agents/scripts/NODEJS?osFamily=LINUX&downloadWith=curl&webServer=NODEJS_DOWNLOAD&flavor=DEFAULT&projectKey=${SEEKER_PROJECT_KEY}&accessToken=${SEEKER_ACCESS_TOKEN}"
                            chmod +x node_installer.sh
                        """
                        // Chạy script, nó sẽ tải về seeker-node-agent.zip
                        sh """
                            ./node_installer.sh
                            mv seeker-node-agent.zip src/paymentservice/seeker-node-agent.zip
                        """

                        // ==================================================================================
                        // 3. GO AGENT (Frontend)
                        // ==================================================================================
                        echo "Downloading Go Agent..."
                        // URL dựa trên hình ảnh image_b6ef84.png
                        sh """
                            curl -k -sSL -o go_installer.sh "${SEEKER_URL}/rest/api/latest/installers/agents/scripts/GO?osFamily=LINUX&downloadWith=curl&webServer=GO_LINUX_AMD64_DEFAULT&flavor=DEFAULT&projectKey=${SEEKER_PROJECT_KEY}&accessToken=${SEEKER_ACCESS_TOKEN}"
                            chmod +x go_installer.sh
                        """
                        // Chạy script, nó sẽ tải về seeker-agent-linux-amd64
                        sh """
                            ./go_installer.sh
                            mv seeker-agent-linux-amd64 src/frontend/seeker-agent-linux-amd64
                        """
                    }
                }
            }
        }

        stage('Build & Push: Java (AdService)') {
            steps {
                script {
                    docker.withRegistry('', "${DOCKER_CRED_ID}") {
                        dir('src/adservice') {
                            // Cần truyền TOKEN vào build args để config lúc runtime
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
                            // Go cần nhiều tham số hơn
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
            echo "--- Cleaning up Agents ---"
            sh "rm -f src/adservice/seeker-agent.jar"
            sh "rm -f src/paymentservice/seeker-node-agent.zip"
            sh "rm -f src/frontend/seeker-agent-linux-amd64"
            sh "rm -f *.sh" // Xóa các script cài đặt tạm
        }
        success {
            echo "✅ Build thành công IAST images với Standard Installer Scripts."
        }
    }
}
