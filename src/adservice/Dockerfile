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

# [FIX PERMISSION] Chuyển sang root để có quyền cài gói hệ thống
USER root

# [FIX SSL/TIME & PROTOBUF]
# 1. Chuyển repo Alpine sang HTTP để tránh lỗi "certificate verify failed" do sai giờ
# 2. Cài đặt thư viện tương thích (libc6-compat, gcompat) để chạy được protoc
RUN sed -i 's/https/http/g' /etc/apk/repositories \
    && apk add --no-cache libc6-compat gcompat

WORKDIR /app

COPY . .

# [OPTIMIZE] Cấu hình RAM và Entropy cho Gradle (Tránh treo)
ENV GRADLE_OPTS="-Dorg.gradle.daemon=false -Dorg.gradle.jvmargs=-Xmx2048m -Djava.security.egd=file:/dev/./urandom"

# [FIX SSL/TIME & REPO - GRADLE]
# Tạo init.gradle cấu hình Mirror HTTP (Aliyun) cho cả Plugin và Dependency
# Thêm repo 'google' để tải protoc
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

# [SEEKER] 1. Copy Agent
COPY seeker-agent.jar /app/seeker-agent.jar

# [SEEKER] 2. Config
ENV SEEKER_SERVER_URL="http://192.168.12.190:8082"
ENV SEEKER_PROJECT_KEY="microservices-demo"
ENV JAVA_TOOL_OPTIONS="-javaagent:/app/seeker-agent.jar"

# Copy kết quả build từ stage trước
COPY --from=builder /app/build/install/hipstershop /app

EXPOSE 9555
ENTRYPOINT ["/app/bin/AdService"]
