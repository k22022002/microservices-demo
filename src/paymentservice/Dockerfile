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

# 1. Cài Python & Tools (Bắt buộc để build thư viện Seeker/Pprof)
RUN sed -i 's/https/http/g' /etc/apk/repositories \
    && apk add --no-cache python3 make g++ unzip tar

RUN npm config set strict-ssl false
ENV NODE_TLS_REJECT_UNAUTHORIZED=0

WORKDIR /usr/src/app
COPY package*.json ./

# Xóa gói debug gây xung đột
RUN sed -i '/@google-cloud\/profiler/d' package.json \
    && sed -i '/@google-cloud\/debug-agent/d' package.json

# 2. Cài App Dependencies
RUN npm install --only=production --no-audit

# 3. [FIX QUAN TRỌNG] Cài Seeker Agent
# File zip này sẽ được Jenkins tải về và đặt vào đây
COPY seeker-node-agent.zip /tmp/agent.zip
RUN unzip -d /tmp/seeker /tmp/agent.zip

# Tìm file .tgz và cài thẳng vào node_modules
RUN find /tmp/seeker -name "seeker-agent.tgz" -exec npm install {} --save --no-audit --prefix . \;

# --- Final Stage ---
FROM node:20-alpine
ENV NODE_TLS_REJECT_UNAUTHORIZED=0
WORKDIR /usr/src/app

# Copy node_modules (Lúc này đã chứa Seeker Agent chuẩn)
COPY --from=builder /usr/src/app/node_modules ./node_modules
COPY . .

# [SEEKER CONFIG]
ARG SEEKER_ACCESS_TOKEN
ENV SEEKER_ACCESS_TOKEN=$SEEKER_ACCESS_TOKEN
ENV SEEKER_SERVER_URL="http://192.168.12.190:8082"
ENV SEEKER_PROJECT_KEY="microservices-demo"

# [FIX PATH] Import từ node_modules
ENV NODE_OPTIONS="--import @synopsys-sig/seeker/agent/index.mjs"

EXPOSE 50051
ENTRYPOINT [ "node", "index.js" ]
