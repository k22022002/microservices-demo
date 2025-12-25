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

# 1. Cài công cụ hỗ trợ
RUN sed -i 's/https/http/g' /etc/apk/repositories \
    && apk add --no-cache python3 make g++ unzip tar

RUN npm config set strict-ssl false
ENV NODE_TLS_REJECT_UNAUTHORIZED=0

WORKDIR /usr/src/app
COPY package*.json ./

# Dọn dẹp package.json
RUN sed -i '/@google-cloud\/profiler/d' package.json \
    && sed -i '/@google-cloud\/debug-agent/d' package.json

# 2. Cài dependencies gốc
RUN npm install --only=production --no-audit

# 3. [DEBUG MODE] Cài Seeker Agent và In Log chi tiết
COPY seeker-node-agent.zip /tmp/agent.zip

# Giải nén và IN RA CẤU TRÚC FILE (Để xem nó nằm ở đâu)
RUN unzip -d /tmp/seeker /tmp/agent.zip && \
    echo "================ KIỂM TRA FILE GIẢI NÉN ================" && \
    ls -R /tmp/seeker && \
    echo "========================================================"

# Tìm và Cài đặt
# Lưu ý: Chúng ta dùng lệnh find để tự tìm file .tgz bất kể nó nằm sâu trong thư mục nào
RUN echo "--- Đang cài đặt Seeker Agent ---" && \
    find /tmp/seeker -name "*.tgz" -exec npm install {} --save --no-audit \;

# [QUAN TRỌNG] Kiểm tra xem cài xong nó chui vào đâu
RUN echo "================ KIỂM TRA NODE_MODULES ================" && \
    ls -F node_modules/ || echo "Khong tim thay node_modules" && \
    echo "--- Kiểm tra folder @synopsys-sig ---" && \
    ls -F node_modules/@synopsys-sig/ || echo "❌ KHÔNG THẤY @synopsys-sig" && \
    echo "========================================================"

# --- Final Stage ---
FROM node:20-alpine
ENV NODE_TLS_REJECT_UNAUTHORIZED=0
WORKDIR /usr/src/app

COPY --from=builder /usr/src/app/node_modules ./node_modules
COPY . .

# Config
ARG SEEKER_ACCESS_TOKEN
ENV SEEKER_ACCESS_TOKEN=$SEEKER_ACCESS_TOKEN
ENV SEEKER_SERVER_URL="http://192.168.12.190:8082"
ENV SEEKER_PROJECT_KEY="microservices-demo"

# Import
ENV NODE_OPTIONS="--import @synopsys-sig/seeker/agent/index.mjs"

EXPOSE 50051
ENTRYPOINT [ "node", "index.js" ]
