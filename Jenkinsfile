pipeline {
    agent any

    environment {
        SEEKER_URL = 'http://192.168.12.190:8082'
        SEEKER_PROJECT_KEY = 'microservices-demo'
        DOCKER_REGISTRY = 'kienngo22022002'
        DOCKER_CRED_ID = 'docker-hub-credentials-id'

        // [FIX 1] Đặt Token ở đây để sửa lỗi "MissingPropertyException"
        // Biến này giờ sẽ dùng được ở cả stage Download và stage Build
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

        stage('Download Seeker Agents (Direct Binary)') {
            steps {
                script {
                    echo "--- Downloading Agents ---"
                    
                    // [FIX 2] Dùng API /binaries/ thay vì /scripts/ để lấy file chuẩn
                    // Thêm cờ -f để báo lỗi ngay nếu server trả về 404/500
                    
                    // 1. JAVA
                    sh """
                        curl -k -fL "${SEEKER_URL}/rest/api/latest/installers/agents/binaries/JAVA?projectKey=${SEEKER_PROJECT_KEY}&accessToken=${SEEKER_ACCESS_TOKEN}" \
                        -o src/adservice/seeker-agent.jar
                    """

                    // 2. NODE.JS (Sửa lỗi MODULE_NOT_FOUND bằng cách tải đúng file zip)
                    sh """
                        curl -k -fL "${SEEKER_URL}/rest/api/latest/installers/agents/binaries/NODEJS?projectKey=${SEEKER_PROJECT_KEY}&accessToken=${SEEKER_ACCESS_TOKEN}" \
                        -o src/paymentservice/seeker-node-agent.zip
                    """
                    
                    // 3. GO
                    sh """
                        curl -k -fL "${SEEKER_URL}/rest/api/latest/installers/agents/binaries/GO?osFamily=LINUX&projectKey=${SEEKER_PROJECT_KEY}&accessToken=${SEEKER_ACCESS_TOKEN}" \
                        -o src/frontend/seeker-agent-linux-amd64
                        chmod +x src/frontend/seeker-agent-linux-amd64
                    """
                }
            }
        }

        stage('Build & Push: Java (AdService)') {
            steps {
                script {
                    docker.withRegistry('', "${DOCKER_CRED_ID}") {
                        dir('src/adservice') {
                            // Truyền Token vào để Agent chạy runtime
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
            // Dọn dẹp
            sh "rm -f src/adservice/seeker-agent.jar"
            sh "rm -f src/paymentservice/seeker-node-agent.zip"
            sh "rm -f src/frontend/seeker-agent-linux-amd64"
        }
    }
}
