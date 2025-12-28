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
RUN sed -i 's/https/http/g' /etc/apk/repositories && apk add --no-cache unzip tar
RUN npm config set strict-ssl false
ENV NODE_TLS_REJECT_UNAUTHORIZED=0

WORKDIR /usr/src/app
COPY package*.json ./

# 1. Cài đặt App Dependencies (Production only)
RUN npm install --only=production --no-audit

# 2. [FIX MANUAL] Giải nén thủ công Seeker Agent
COPY seeker-node-agent.zip /tmp/seeker-node-agent.zip
RUN unzip -d /tmp/seeker /tmp/seeker-node-agent.zip

# Tìm file tgz và giải nén nó ra thư mục /usr/src/app/seeker-agent
# (Mặc định npm pack tạo thư mục tên là 'package', ta đổi tên nó thành 'seeker-agent')
RUN mkdir -p /usr/src/app/seeker-agent \
    && find /tmp/seeker -name "seeker-agent.tgz" -exec tar -xzf {} -C /usr/src/app/seeker-agent --strip-components=1 \; \
    # Cài đặt dependencies RIÊNG cho agent
    && cd /usr/src/app/seeker-agent && npm install --production --no-audit

# --- Final Stage ---
FROM node:20-alpine
ENV NODE_TLS_REJECT_UNAUTHORIZED=0
WORKDIR /usr/src/app

# Copy node_modules của App
COPY --from=builder /usr/src/app/node_modules ./node_modules

# [QUAN TRỌNG] Copy thư mục Agent đã giải nén thủ công
COPY --from=builder /usr/src/app/seeker-agent ./seeker-agent

COPY . .

# [SEEKER] Config
ARG SEEKER_ACCESS_TOKEN
ENV SEEKER_ACCESS_TOKEN=$SEEKER_ACCESS_TOKEN
ENV SEEKER_SERVER_URL="http://192.168.12.190:8082"
ENV SEEKER_PROJECT_KEY="microservices-demo"

# [FIX PATH] Trỏ thẳng vào file index.mjs trong thư mục đã giải nén
# Không dùng @synopsys-sig... nữa mà dùng đường dẫn file trực tiếp
ENV NODE_OPTIONS="--import /usr/src/app/seeker-agent/agent/index.mjs"

EXPOSE 50051
ENTRYPOINT [ "node", "index.js" ]
