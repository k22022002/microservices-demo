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
RUN apk add --no-cache libc6-compat gcompat

WORKDIR /app
COPY . .

# Giải nén gói Agent
COPY seeker-agent.jar /tmp/seeker-bundle.zip
RUN mkdir -p /tmp/extracted && \
    cd /tmp/extracted && \
    jar xf /tmp/seeker-bundle.zip && \
    find . -name "seeker-agent.jar" -exec cp {} /tmp/real-agent.jar \;

# Build Project
ENV GRADLE_OPTS="-Dorg.gradle.daemon=false -Dorg.gradle.jvmargs=-Xmx2048m -Djava.security.egd=file:/dev/./urandom"
RUN gradle installDist -x test --no-daemon --info --stacktrace

# --- Final Stage ---
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

# Copy Seeker Agent
COPY --from=builder /tmp/real-agent.jar /app/seeker-agent.jar

# Cấu hình Seeker Agent
ARG SEEKER_ACCESS_TOKEN
ENV SEEKER_ACCESS_TOKEN=$SEEKER_ACCESS_TOKEN
ENV SEEKER_SERVER_URL="http://192.168.12.190:8082"
ENV SEEKER_PROJECT_KEY="microservices-demo-java"
ENV JAVA_TOOL_OPTIONS="-javaagent:/app/seeker-agent.jar"

COPY --from=builder /app/build/install/hipstershop /app

EXPOSE 9555
ENTRYPOINT ["/app/bin/AdService"]
