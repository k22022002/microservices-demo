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

WORKDIR /app

COPY . .

# [FIX SSL/TIME]
# Cập nhật init.gradle: 
# 1. Thêm 'pluginManagement' để tải Plugin qua HTTP Aliyun (Sửa lỗi protobuf not found)
# 2. Giữ nguyên cấu hình 'allprojects' cho dependencies thường
# 3. Tạo file tại /tmp/init.gradle để tránh lỗi permission
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
        }\n\
    }\n\
    repositories {\n\
        maven {\n\
            url = uri('http://maven.aliyun.com/repository/public')\n\
            allowInsecureProtocol = true\n\
        }\n\
    }\n\
}\n" > /tmp/init.gradle \
 && gradle installDist -x test --no-daemon --init-script /tmp/init.gradle

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
