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

# 2. Xóa các gói Google gây lỗi khỏi package.json
RUN sed -i '/@google-cloud\/profiler/d' package.json \
    && sed -i '/@google-cloud\/debug-agent/d' package.json \
    && sed -i '/@google-cloud\/trace-agent/d' package.json

# 3. Cài dependencies thật
RUN npm install --only=production --no-audit

# 4. Cài Seeker Agent
COPY seeker-node-agent.zip /tmp/agent.zip
RUN unzip -d /tmp/seeker /tmp/agent.zip
RUN npm install /tmp/seeker/*.tgz --save --no-audit --prefix /usr/src/app

# --- Final Stage ---
FROM node:20-alpine
ENV NODE_TLS_REJECT_UNAUTHORIZED=0
WORKDIR /usr/src/app

# Copy node_modules từ builder
COPY --from=builder /usr/src/app/node_modules ./node_modules
COPY . .

# 5. TẠO MODULE GIẢ (BẤT TỬ)
# Giữ nguyên phần này vì nó đã hoạt động Tốt
RUN mkdir -p node_modules/@google-cloud/profiler \
    && echo "module.exports = { start: function() { console.log('Mock Profiler'); return {}; } };" > node_modules/@google-cloud/profiler/index.js

RUN mkdir -p node_modules/@google-cloud/debug-agent \
    && echo "module.exports = { start: function() { console.log('Mock Debugger'); return {}; } };" > node_modules/@google-cloud/debug-agent/index.js

RUN mkdir -p node_modules/@google-cloud/trace-agent \
    && echo "module.exports = { start: function() { console.log('Mock Tracer'); return {}; } };" > node_modules/@google-cloud/trace-agent/index.js

# Config Seeker
ARG SEEKER_ACCESS_TOKEN
ENV SEEKER_ACCESS_TOKEN=$SEEKER_ACCESS_TOKEN
ENV SEEKER_SERVER_URL="http://192.168.12.190:8082"
ENV SEEKER_PROJECT_KEY="microservices-demo"
ENV NODE_OPTIONS="--require @synopsys-sig/seeker"

# [FIX FINAL] Cài cứng Port để tránh lỗi undefined
ENV PORT=50051

EXPOSE 50051
ENTRYPOINT [ "node", "index.js" ]
