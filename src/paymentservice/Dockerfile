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

# Setup cơ bản
RUN sed -i 's/https/http/g' /etc/apk/repositories && apk add --no-cache unzip
RUN npm config set strict-ssl false
ENV NODE_TLS_REJECT_UNAUTHORIZED=0

WORKDIR /usr/src/app
COPY package*.json ./

# Xóa các gói gây xung đột (nếu có)
RUN sed -i '/@google-cloud\/profiler/d' package.json \
    && sed -i '/@google-cloud\/debug-agent/d' package.json

# [SEEKER] Cài đặt Agent
COPY seeker-node-agent.zip /tmp/seeker-node-agent.zip

# 1. Giải nén
RUN unzip -d /tmp/seeker /tmp/seeker-node-agent.zip

# 2. [FIX CRITICAL] Cài đặt Agent vào Root node_modules với tham số --prefix
#    Lỗi cũ: "npm install run without required argument --prefix"
#    Giải pháp: Thêm "--prefix /usr/src/app"
RUN find /tmp/seeker -name "seeker-agent.tgz" -exec npm install {} --prefix /usr/src/app --save --no-audit \;

# 3. Cài đặt App Dependencies (Production only)
RUN npm install --only=production --no-audit

# --- Final Stage ---
FROM node:20-alpine
ENV NODE_TLS_REJECT_UNAUTHORIZED=0
WORKDIR /usr/src/app

# Copy node_modules của App (Đã bao gồm Seeker Agent bên trong)
COPY --from=builder /usr/src/app/node_modules ./node_modules

COPY . .

# [SEEKER] Config
ARG SEEKER_ACCESS_TOKEN
ENV SEEKER_ACCESS_TOKEN=$SEEKER_ACCESS_TOKEN
ENV SEEKER_SERVER_URL="http://192.168.12.190:8082"
ENV SEEKER_PROJECT_KEY="microservices-demo"

# [FIX PATH] Sử dụng import chuẩn từ node_modules
# Vì đã cài vào root, ta không cần đường dẫn dài dòng "/usr/src/app/seeker/..." nữa
ENV NODE_OPTIONS="--import @synopsys-sig/seeker/agent/index.mjs"

EXPOSE 50051
ENTRYPOINT [ "node", "index.js" ]
