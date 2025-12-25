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
USER root
# Chuyển repo sang HTTP
RUN sed -i 's/https/http/g' /etc/apk/repositories && apk add --no-cache libc6-compat gcompat
WORKDIR /app
COPY . .
# Optimize Gradle
ENV GRADLE_OPTS="-Dorg.gradle.daemon=false -Dorg.gradle.jvmargs=-Xmx2048m -Djava.security.egd=file:/dev/./urandom"
# (Giữ nguyên phần config repo Gradle của bạn ở đây...)
RUN printf "settingsEvaluated { settings -> settings.pluginManagement { repositories { maven { url = uri('http://maven.aliyun.com/repository/gradle-plugin'); allowInsecureProtocol = true } } } }\n allprojects { repositories { maven { url = uri('http://maven.aliyun.com/repository/public'); allowInsecureProtocol = true } } }" > /tmp/init.gradle \
 && gradle installDist -x test --no-daemon --init-script /tmp/init.gradle

# --- Final Stage ---
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app

# [QUAN TRỌNG] Copy file agent
COPY seeker-agent.jar /app/seeker-agent.jar

# [DEBUG] Kiểm tra file ngay trong quá trình build
# Nếu file nhỏ hơn 1MB (do lỗi copy) hoặc không unzip được -> Dừng build ngay!
RUN ls -lh /app/seeker-agent.jar && \
    apk add --no-cache unzip && \
    unzip -t /app/seeker-agent.jar || \
    (echo "❌ LỖI: File seeker-agent.jar trong Docker bị hỏng!" && exit 1)

# Config Seeker
ARG SEEKER_ACCESS_TOKEN
ENV SEEKER_ACCESS_TOKEN=$SEEKER_ACCESS_TOKEN
ENV SEEKER_SERVER_URL="http://192.168.12.190:8082"
ENV SEEKER_PROJECT_KEY="microservices-demo"
ENV JAVA_TOOL_OPTIONS="-javaagent:/app/seeker-agent.jar"

COPY --from=builder /app/build/install/hipstershop /app
EXPOSE 9555
ENTRYPOINT ["/app/bin/AdService"]
