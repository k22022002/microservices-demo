# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# --- Builder Stage ---
FROM gradle:8.6-jdk21-alpine AS builder

# [FIX PERMISSION]
USER root
# Chuyển repo sang HTTP
RUN sed -i 's/https/http/g' /etc/apk/repositories \
    && apk add --no-cache libc6-compat gcompat

WORKDIR /app
COPY . .

# =========================================================================
# [FIX CRITICAL] GIẢI NÉN GÓI AGENT
# =========================================================================

# 1. Copy file tải từ Jenkins vào (File này thực chất là 1 file ZIP 12MB)
COPY seeker-agent.jar /tmp/seeker-bundle.zip

# 2. Dùng lệnh 'jar' của JDK để giải nén
#    Lệnh này có sẵn, không cần cài unzip -> Tránh lỗi mạng SSL
RUN mkdir -p /tmp/extracted && \
    cd /tmp/extracted && \
    # Giải nén
    jar xf /tmp/seeker-bundle.zip && \
    # In ra để debug xem bên trong có gì
    echo "--- Nội dung gói tải về ---" && \
    ls -R /tmp/extracted && \
    # Tự động tìm file seeker-agent.jar thật và copy ra /tmp/real-agent.jar
    find . -name "seeker-agent.jar" -exec cp {} /tmp/real-agent.jar \;

# =========================================================================

# [OPTIMIZE] Gradle
ENV GRADLE_OPTS="-Dorg.gradle.daemon=false -Dorg.gradle.jvmargs=-Xmx2048m -Djava.security.egd=file:/dev/./urandom"

# [FIX SSL/TIME & REPO - GRADLE] (Giữ nguyên cấu hình của bạn)
RUN printf "\
settingsEvaluated { settings ->\n\
    settings.pluginManagement {\n\
        repositories {\n\
            maven {\n\
                url = uri('http://maven.aliyun.com/repository/gradle-plugin')\n\
                allowInsecureProtocol = true\n\
            }\n\
            maven {\n\
                url = uri('http://maven.aliyun.com/repository/public')\n\
                allowInsecureProtocol = true\n\
            }\n\
        }\n\
    }\n\
}\n\
allprojects {\n\
    buildscript {\n\
        repositories {\n\
            maven {\n\
                url = uri('http://maven.aliyun.com/repository/public')\n\
                allowInsecureProtocol = true\n\
            }\n\
            maven {\n\
                url = uri('http://maven.aliyun.com/repository/google')\n\
                allowInsecureProtocol = true\n\
            }\n\
        }\n\
    }\n\
    repositories {\n\
        maven {\n\
            url = uri('http://maven.aliyun.com/repository/public')\n\
            allowInsecureProtocol = true\n\
        }\n\
        maven {\n\
            url = uri('http://maven.aliyun.com/repository/google')\n\
            allowInsecureProtocol = true\n\
        }\n\
    }\n\
}\n" > /tmp/init.gradle \
 && gradle installDist -x test --no-daemon --info --stacktrace --init-script /tmp/init.gradle

# --- Final Stage ---
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

# [SEEKER] COPY FILE AGENT THẬT (Đã được giải nén ở trên)
# Lưu ý: Chúng ta lấy file /tmp/real-agent.jar từ builder
COPY --from=builder /tmp/real-agent.jar /app/seeker-agent.jar

# [SEEKER] Config
ARG SEEKER_ACCESS_TOKEN
ENV SEEKER_ACCESS_TOKEN=$SEEKER_ACCESS_TOKEN
ENV SEEKER_SERVER_URL="http://192.168.12.190:8082"
ENV SEEKER_PROJECT_KEY="microservices-demo-java"

# [SEEKER] Kích hoạt Agent
ENV JAVA_TOOL_OPTIONS="-javaagent:/app/seeker-agent.jar"

COPY --from=builder /app/build/install/hipstershop /app

EXPOSE 9555
ENTRYPOINT ["/app/bin/AdService"]
