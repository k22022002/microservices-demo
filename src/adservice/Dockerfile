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
FROM gradle:8.6-jdk21-alpine AS builder

WORKDIR /app

COPY . .

# Chạy build bằng gradle có sẵn (Bỏ qua test để nhanh hơn)
# Lưu ý: Lệnh này sẽ tạo ra thư mục build/install/hipstershop
RUN gradle installDist -x test --no-daemon

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
