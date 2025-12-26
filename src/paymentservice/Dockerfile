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

# Dọn dẹp package.json
RUN sed -i '/@google-cloud\/profiler/d' package.json \
    && sed -i '/@google-cloud\/debug-agent/d' package.json

# 2. Cài dependencies gốc
RUN npm install --only=production --no-audit

# 3. [FIXED] Cài Seeker Agent với tham số Prefix
COPY seeker-node-agent.zip /tmp/agent.zip

# Giải nén
RUN unzip -d /tmp/seeker /tmp/agent.zip

# Cài đặt file .tgz với tham số --prefix /usr/src/app
# Đây là chìa khóa để sửa lỗi "npm install run without required argument"
RUN echo "--- Đang cài đặt file .tgz ---" && \
    npm install /tmp/seeker/*.tgz --save --no-audit --prefix /usr/src/app

# --- Final Stage ---
FROM node:20-alpine
ENV NODE_TLS_REJECT_UNAUTHORIZED=0
WORKDIR /usr/src/app

# Copy node_modules (Lúc này đã chứa Seeker Agent được cài đúng chỗ)
COPY --from=builder /usr/src/app/node_modules ./node_modules
COPY . .

# [KIỂM TRA] In ra xem nó cài vào đâu (Debug)
RUN echo "--- Kiểm tra thư mục Agent ---" && \
    ls -F node_modules/@synopsys-sig/ || \
    ls -F node_modules/@seeker/ || \
    echo "⚠️ Vẫn chưa thấy, cần kiểm tra log cài đặt!"

ARG SEEKER_ACCESS_TOKEN
ENV SEEKER_ACCESS_TOKEN=$SEEKER_ACCESS_TOKEN
ENV SEEKER_SERVER_URL="http://192.168.12.190:8082"
ENV SEEKER_PROJECT_KEY="microservices-demo"

# [FIX PATH] Đường dẫn chuẩn sau khi cài bằng npm install
# Thông thường nó sẽ nằm trong @synopsys-sig/seeker HOẶC @seeker/agent tùy phiên bản
# Ta dùng đường dẫn phổ biến nhất hiện nay:
ENV NODE_OPTIONS="--import @synopsys-sig/seeker/agent/index.mjs"

EXPOSE 50051
ENTRYPOINT [ "node", "index.js" ]
