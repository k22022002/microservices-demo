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

# --- Builder Stage (Giữ nguyên phần đầu của bạn) ---
# --- Builder Stage ---
# --- Builder Stage ---
# --- Builder Stage: Dùng image có sẵn Gradle để không bị lỗi tải về ---
# --- Builder Stage ---
FROM eclipse-temurin:21-jdk-alpine AS builder

WORKDIR /app

COPY ["build.gradle", "gradlew", "./"]
COPY gradle gradle
RUN chmod +x gradlew

# [FIX SSL] Tải Gradle thủ công dùng wget không check chứng chỉ
# Dùng server khác (mirror) nếu server chính quá chậm
RUN sed -i 's/https/http/g' /etc/apk/repositories \
    && apk add --no-cache wget unzip \
    && echo "Downloading Gradle..." \
    && wget --no-check-certificate -q https://services.gradle.org/distributions/gradle-8.5-bin.zip -P /tmp \
    && unzip -q /tmp/gradle-8.5-bin.zip -d /root/.gradle/wrapper/dists/gradle-8.5-bin/ \
    && mkdir -p /root/.gradle/wrapper/dists/gradle-8.5-bin/oz20x72052e379u313f509931/ \
    && mv /root/.gradle/wrapper/dists/gradle-8.5-bin/gradle-8.5 /root/.gradle/wrapper/dists/gradle-8.5-bin/oz20x72052e379u313f509931/

COPY . .

# Chạy build (Gradle sẽ tìm thấy bản đã tải và không cần tải lại)
RUN ./gradlew installDist -x test --no-daemon

# --- Final Stage ---
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

# [SEEKER] Copy Agent
COPY seeker-agent.jar /app/seeker-agent.jar

# [SEEKER] Config
ENV SEEKER_SERVER_URL="http://192.168.12.190:8082"
ENV SEEKER_PROJECT_KEY="microservices-demo"
ENV JAVA_TOOL_OPTIONS="-javaagent:/app/seeker-agent.jar"

COPY --from=builder /app .

EXPOSE 9555
ENTRYPOINT ["/app/build/install/hipstershop/bin/AdService"]
