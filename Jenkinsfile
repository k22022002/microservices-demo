pipeline {
    agent any

    environment {
        SEEKER_URL = 'http://192.168.12.190:8082'
        SEEKER_PROJECT_KEY = 'microservices-demo'
        DOCKER_REGISTRY = 'kienngo22022002'
        DOCKER_CRED_ID = 'docker-hub-credentials-id'
        
        // [QUAN TRỌNG] Lấy Token ở đây để dùng được cho TOÀN BỘ các stages (Download + Build)
        SEEKER_ACCESS_TOKEN = credentials('seeker-agent-token')

        // Cấu hình bypass SSL
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
                    echo "--- Downloading Agent Binaries Directly ---"

                    // 1. JAVA AGENT (AdService)
                    sh """
                       curl -k -fL "${SEEKER_URL}/rest/api/latest/installers/agents/binaries/JAVA?projectKey=${SEEKER_PROJECT_KEY}&accessToken=${SEEKER_ACCESS_TOKEN}" \
                       -o seeker-agent.jar
                       
                       # Di chuyển vào thư mục build context
                       mv seeker-agent.jar src/adservice/seeker-agent.jar
                    """

                    // 2. NODE.JS AGENT (PaymentService)
                    sh """
                       curl -k -fL "${SEEKER_URL}/rest/api/latest/installers/agents/binaries/NODEJS?projectKey=${SEEKER_PROJECT_KEY}&accessToken=${SEEKER_ACCESS_TOKEN}" \
                       -o seeker-node-agent.zip
                       
                       # Di chuyển vào thư mục build context
                       mv seeker-node-agent.zip src/paymentservice/seeker-node-agent.zip
                    """

                    // 3. GO AGENT (Frontend)
                    sh """
                       curl -k -fL "${SEEKER_URL}/rest/api/latest/installers/agents/binaries/GO?osFamily=LINUX&projectKey=${SEEKER_PROJECT_KEY}&accessToken=${SEEKER_ACCESS_TOKEN}" \
                       -o seeker-agent-linux-amd64
                       
                       chmod +x seeker-agent-linux-amd64
                       # Di chuyển vào thư mục build context
                       mv seeker-agent-linux-amd64 src/frontend/seeker-agent-linux-amd64
                    """
                }
            }
        }

        stage('Build & Push: Java (AdService)') {
            steps {
                script {
                    docker.withRegistry('', "${DOCKER_CRED_ID}") {
                        dir('src/adservice') {
                            // Bây giờ biến SEEKER_ACCESS_TOKEN đã có thể truy cập ở đây
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
            // Xóa file agent để tránh rác (dùng -f để không lỗi nếu file không tồn tại)
            sh "rm -f src/adservice/seeker-agent.jar"
            sh "rm -f src/paymentservice/seeker-node-agent.zip"
            sh "rm -f src/frontend/seeker-agent-linux-amd64"
        }
        success {
            echo "✅ Build thành công IAST images."
        }
    }
}
