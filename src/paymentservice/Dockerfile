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
FROM node:20-alpine AS builder

# 1. Cài tools
RUN sed -i 's/https/http/g' /etc/apk/repositories \
    && apk add --no-cache python3 make g++ unzip tar

RUN npm config set strict-ssl false
ENV NODE_TLS_REJECT_UNAUTHORIZED=0

WORKDIR /usr/src/app
COPY package*.json ./

# Dọn dẹp
RUN sed -i '/@google-cloud\/profiler/d' package.json \
    && sed -i '/@google-cloud\/debug-agent/d' package.json

# 2. Cài dependencies
RUN npm install --only=production --no-audit

# 3. [FIX CỨNG] Cài Seeker Agent (Chấp nhận mọi tên file)
COPY seeker-node-agent.zip /tmp/agent.zip

# Giải nén
RUN unzip -d /tmp/seeker /tmp/agent.zip

# IN RA file để kiểm tra (Xem tên thật nó là gì)
RUN echo "--- DANH SÁCH FILE GIẢI NÉN ĐƯỢC ---" && \
    ls -R /tmp/seeker

# Cài đặt bằng lệnh Wildcard (*) để không bị sai tên
# Lệnh này sẽ cài bất cứ file .tgz nào nó thấy
RUN echo "--- Đang cài đặt file .tgz ---" && \
    npm install /tmp/seeker/*.tgz --save --no-audit

# --- Final Stage ---
FROM node:20-alpine
ENV NODE_TLS_REJECT_UNAUTHORIZED=0
WORKDIR /usr/src/app

COPY --from=builder /usr/src/app/node_modules ./node_modules
COPY . .

# [KIỂM TRA LẠI] In ra để chắc chắn agent đã nằm trong node_modules
RUN echo "--- Kiểm tra kết quả cài đặt ---" && \
    ls -d node_modules/@synopsys-sig/seeker || \
    ls -d node_modules/seeker-agent || \
    echo "⚠️ Vẫn chưa thấy Agent, hãy kiểm tra log!"

ARG SEEKER_ACCESS_TOKEN
ENV SEEKER_ACCESS_TOKEN=$SEEKER_ACCESS_TOKEN
ENV SEEKER_SERVER_URL="http://192.168.12.190:8082"
ENV SEEKER_PROJECT_KEY="microservices-demo"

# Tạm thời disable dòng này để Container chạy được lên đã (rồi tính tiếp)
# ENV NODE_OPTIONS="--import @synopsys-sig/seeker/agent/index.mjs"

EXPOSE 50051
ENTRYPOINT [ "node", "index.js" ]
