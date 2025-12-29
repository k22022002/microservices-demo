pipeline {
    agent any

    environment {
        // --- CẤU HÌNH SEEKER & DOCKER ---
        SEEKER_URL = 'http://192.168.12.190:8082'
        SEEKER_PROJECT_KEY = 'microservices-demo'
        DOCKER_REGISTRY = 'kienngo22022002'
        DOCKER_CRED_ID = 'docker-hub-credentials-id'

        // --- FIX LỖI SSL & TIME (QUAN TRỌNG) ---
        // Tắt kiểm tra SSL cho Git (tránh lỗi khi clone code)
        GIT_SSL_NO_VERIFY = '1'
        // Tắt kiểm tra SSL cho các lệnh Node.js/NPM nếu chạy trên agent
        NODE_TLS_REJECT_UNAUTHORIZED = '0'
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Cấu hình git global để chắc chắn không check SSL trước khi checkout
                sh 'git config --global http.sslVerify false'
                checkout scm
            }
        }

        stage('Download Seeker Agents (Bypass SSL)') {
            steps {
                script {
                    echo "--- Downloading Agents (Ignoring SSL/Time errors) ---"
                    
                    // 1. JAVA: Tải vào src/adservice để Dockerfile COPY
                    // Sử dụng cờ -k để bỏ qua kiểm tra chứng chỉ
                    sh """
                        curl -k -X GET -fL "${SEEKER_URL}/rest/api/latest/installers/agents/binaries/JAVA?projectKey=${SEEKER_PROJECT_KEY}" \
                        -o src/adservice/seeker-agent.jar
                    """

                    // 2. NODE.JS: Tải vào src/paymentservice
                    sh """
                        curl -k -X GET -fL "${SEEKER_URL}/rest/api/latest/installers/agents/binaries/NODEJS?projectKey=${SEEKER_PROJECT_KEY}" \
                        -o src/paymentservice/seeker-node-agent.zip
                    """
                    
                    // 3. GO: Tải vào src/frontend
                    // Lưu ý: Dockerfile Go của bạn mong đợi tên file là 'seeker-agent-linux-amd64'
                    sh """
                        curl -k -X GET -fL "${SEEKER_URL}/rest/api/latest/installers/agents/binaries/GO?osFamily=LINUX&projectKey=${SEEKER_PROJECT_KEY}" \
                        -o src/frontend/seeker-agent-linux-amd64
                    """
                }
            }
        }

        stage('Build & Push: Java (AdService)') {
            steps {
                script {
                    docker.withRegistry('', "${DOCKER_CRED_ID}") {
                        // Dockerfile đã có lệnh COPY seeker-agent.jar
                        // Lưu ý: Đảm bảo file Dockerfile.txt đã được đổi tên thành Dockerfile trong thư mục src/adservice
                        dir('src/adservice') {
                            def img = docker.build("${DOCKER_REGISTRY}/adservice:iast", ".")
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
                        // Dockerfile đã có lệnh COPY seeker-node-agent.zip
                        dir('src/paymentservice') {
                            def img = docker.build("${DOCKER_REGISTRY}/paymentservice:iast", ".")
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
                        // Dockerfile Go cần Build Args để chạy IAST tool lúc build
                        dir('src/frontend') {
                            def img = docker.build("${DOCKER_REGISTRY}/frontend:iast", 
                                "--build-arg SEEKER_URL=${SEEKER_URL} --build-arg SEEKER_PROJECT=${SEEKER_PROJECT_KEY} .")
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
            // Xóa file agent để tránh commit nhầm vào git sau này
            sh "rm -f src/adservice/seeker-agent.jar"
            sh "rm -f src/paymentservice/seeker-node-agent.zip"
            sh "rm -f src/frontend/seeker-agent-linux-amd64"
        }
        success {
            echo "✅ Build thành công IAST images. Hệ thống đã bypass SSL/Time check."
        }
    }
}
