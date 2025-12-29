pipeline {
    agent any

    environment {
        // Cấu hình chung
        SEEKER_URL = 'http://192.168.12.190:8082'
        SEEKER_PROJECT_KEY = 'microservices-demo'
        DOCKER_REGISTRY = 'k22022002'
        DOCKER_CRED_ID = 'docker-hub-credentials-id'
        
        // Token (Nếu cần xác thực khi tải file, dùng biến này trong lệnh curl)
        // Hiện tại lệnh curl bên dưới đang để trống &accessToken=, bạn có thể điền vào nếu server bắt buộc
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Download Seeker Agents') {
            steps {
                script {
                    echo "--- Downloading Agents ---"
                    
                    // 1. JAVA (.jar) - Cho AdService
                    // Tải thẳng vào thư mục src/adservice
                    sh """
                        curl -k -X GET -fL "${SEEKER_URL}/rest/api/latest/installers/agents/binaries/JAVA?projectKey=${SEEKER_PROJECT_KEY}" \
                        -o src/adservice/seeker-agent.jar
                    """

                    // 2. NODE.JS (.zip) - Cho PaymentService
                    // Tải script cài đặt như hình bạn gửi, nhưng ta chỉ lấy file zip thôi
                    // API tải file zip trực tiếp:
                    sh """
                        curl -k -X GET -fL "${SEEKER_URL}/rest/api/latest/installers/agents/binaries/NODEJS?projectKey=${SEEKER_PROJECT_KEY}" \
                        -o src/paymentservice/seeker-node-agent.zip
                    """
                    
                    // 3. GO (Binary) - Cho Frontend
                    // Tải theo tham số osFamily=LINUX như hình
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
                        // File jar đã nằm trong src/adservice, Dockerfile chỉ cần COPY
                        def img = docker.build("${DOCKER_REGISTRY}/adservice:iast", "./src/adservice")
                        img.push()
                    }
                }
            }
        }

        stage('Build & Push: Node.js (PaymentService)') {
            steps {
                script {
                    docker.withRegistry('', "${DOCKER_CRED_ID}") {
                        // File zip đã nằm trong src/paymentservice
                        def img = docker.build("${DOCKER_REGISTRY}/paymentservice:iast", "./src/paymentservice")
                        img.push()
                    }
                }
            }
        }

        stage('Build & Push: Go (Frontend)') {
            steps {
                script {
                    docker.withRegistry('', "${DOCKER_CRED_ID}") {
                        // File binary đã nằm trong src/frontend
                        // Truyền biến môi trường vào Build Arg để Seeker Build Tool hoạt động
                        def img = docker.build("${DOCKER_REGISTRY}/frontend:iast", 
                            "--build-arg SEEKER_URL=${SEEKER_URL} --build-arg SEEKER_PROJECT=${SEEKER_PROJECT_KEY} ./src/frontend")
                        img.push()
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
        }
        success {
            echo "✅ Build thành công. Hãy deploy các image tag :iast và tạo traffic để kiểm tra."
        }
    }
}
