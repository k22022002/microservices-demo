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
FROM eclipse-temurin:21-jdk-alpine AS builder

WORKDIR /app

# [FIX SSL/TIME] 1. Chuyen repo Alpine sang HTTP
RUN sed -i 's/https/http/g' /etc/apk/repositories

# [FIX SSL/TIME] 2. Cai dat cac cong cu can thiet
RUN apk add --no-cache wget unzip

# [FIX SSL/TIME] 3. Cai dat Gradle 8.5 thu cong (Bo qua Wrapper)
RUN wget --no-check-certificate -q https://services.gradle.org/distributions/gradle-8.5-bin.zip -P /tmp \
    && unzip -q /tmp/gradle-8.5-bin.zip -d /opt/ \
    && ln -s /opt/gradle-8.5 /opt/gradle

# Them Gradle vao PATH
ENV PATH=$PATH:/opt/gradle/bin

# [FIX SSL/TIME] 4. Tao file init.gradle de ep buoc tai thu vien qua HTTP (Aliyun Mirror)
# Dieu nay giup tranh loi PKIX path validation failed khi build app
RUN mkdir -p /root/.gradle && echo " \
    allprojects { \
        buildscript { \
            repositories { \
                maven { url 'http://maven.aliyun.com/repository/public'; allowInsecureProtocol = true } \
                maven { url 'http://maven.aliyun.com/repository/gradle-plugin'; allowInsecureProtocol = true } \
            } \
        } \
        repositories { \
            maven { url 'http://maven.aliyun.com/repository/public'; allowInsecureProtocol = true } \
        } \
    } \
" > /root/.gradle/init.gradle

COPY . .

# [FIX SSL/TIME] 5. Chay build bang lenh gradle truc tiep (khong dung ./gradlew)
RUN gradle installDist -x test --no-daemon

# --- Final Stage ---
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

# [SEEKER] Copy Agent
COPY seeker-agent.jar /app/seeker-agent.jar

# [SEEKER] Config
ENV SEEKER_SERVER_URL="http://192.168.12.190:8082"
ENV SEEKER_PROJECT_KEY="microservices-demo"
ENV JAVA_TOOL_OPTIONS="-javaagent:/app/seeker-agent.jar"

COPY --from=builder /app/build/install/hipstershop /app

EXPOSE 9555
ENTRYPOINT ["/app/bin/AdService"]
