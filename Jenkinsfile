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

        stage('Download Seeker Agents (Direct Binary)') {
            steps {
                script {
                    echo "--- Downloading Agents with Check ---"

		    // 1. JAVA: Xóa file cũ
                    sh "rm -f src/adservice/seeker-agent.jar"
                    
                    // Tải file
                    sh """
                        curl -k -L "${SEEKER_URL}/rest/api/latest/installers/agents/binaries/JAVA?projectKey=microservices-demo-java&accessToken=${SEEKER_ACCESS_TOKEN}" \
                        -o src/adservice/seeker-agent.jar
                    """
                    
                    // [QUAN TRỌNG] Kiểm tra xem file tải về chứa cái gì
                    sh """
                        echo "--- KIỂM TRA FILE JAVA AGENT ---"
                        # Lệnh 'file' giúp xem loại file (HTML hay Zip data)
                        # Nếu không có lệnh file thì dùng cat để in nội dung
                        if unzip -t src/adservice/seeker-agent.jar > /dev/null 2>&1; then
                            echo "✅ SUCCESS: File JAR tải về OK."
                        else
                            echo "❌ ERROR: File tải về KHÔNG PHẢI là JAR. Nội dung thực tế là:"
                            echo "======================================================="
                            cat src/adservice/seeker-agent.jar
                            echo "======================================================="
                            echo "Dừng build để bạn kiểm tra lỗi trên."
                            exit 1
                        fi
                    """
                    // 2. NODE.JS
                    sh """
                        curl -k -fL "${SEEKER_URL}/rest/api/latest/installers/agents/binaries/NODEJS?projectKey=microservices-demo-nodejs&accessToken=${SEEKER_ACCESS_TOKEN}" \
                        -o src/paymentservice/seeker-node-agent.zip
                        
                        if unzip -t src/paymentservice/seeker-node-agent.zip; then
                            echo "Node Agent downloaded successfully"
                        else
                            echo "ERROR: Node Agent file is corrupted!"
                            exit 1
                        fi
                    """
                    
                    // 3. GO
                    sh """
                        curl -k -fL "${SEEKER_URL}/rest/api/latest/installers/agents/binaries/GO?osFamily=LINUX&projectKey=microservices-demo-go&accessToken=${SEEKER_ACCESS_TOKEN}" \
                        -o src/frontend/seeker-agent-linux-amd64
                        chmod +x src/frontend/seeker-agent-linux-amd64
                    """
		    sh "curl -k -fL '${SEEKER_URL}/rest/api/latest/installers/agents/binaries/GO?osFamily=LINUX&projectKey=microservices-demo-go&accessToken=${SEEKER_ACCESS_TOKEN}' -o src/checkoutservice/seeker-agent-linux-amd64"
                    sh "chmod +x src/checkoutservice/seeker-agent-linux-amd64"
                }
            }
        }

        stage('Build & Push: Java (AdService)') {
            steps {
                script {
                    docker.withRegistry('', "${DOCKER_CRED_ID}") {
                        dir('src/adservice') {
                            // --no-cache để đảm bảo copy file agent mới nhất
                            def img = docker.build("${DOCKER_REGISTRY}/adservice:iast", 
                                "--no-cache --build-arg SEEKER_ACCESS_TOKEN=${SEEKER_ACCESS_TOKEN} .")
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
                                "--no-cache --build-arg SEEKER_ACCESS_TOKEN=${SEEKER_ACCESS_TOKEN} .")
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
                            def img = docker.build("${DOCKER_REGISTRY}/checkoutservice:iast", 
                                "--no-cache --build-arg SEEKER_URL=${SEEKER_URL} --build-arg SEEKER_PROJECT=${SEEKER_PROJECT_KEY} --build-arg SEEKER_ACCESS_TOKEN=${SEEKER_ACCESS_TOKEN} .")
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
                            // [QUAN TRỌNG] Truyền ARG từ biến môi trường của Jenkins vào đây
                            def img = docker.build("${DOCKER_REGISTRY}/frontend:iast", 
                                "--no-cache \
                                --build-arg SEEKER_URL=${SEEKER_URL} \
                                --build-arg SEEKER_PROJECT=microservices-demo-go \
                                --build-arg SEEKER_ACCESS_TOKEN=${SEEKER_ACCESS_TOKEN} \
                                .")
                            
                            // Nếu lỗi SSL không push được thì comment dòng này lại
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
	    sh "rm -f src/checkoutservice/seeker-agent-linux-amd64"
        }
    }
}
