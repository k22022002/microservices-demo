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

RUN apk add --update --no-cache python3 make g++ unzip tar

WORKDIR /usr/src/app
COPY package*.json ./

ENV NODE_TLS_REJECT_UNAUTHORIZED=0
RUN npm config set strict-ssl false \
    && npm config set registry http://registry.npmjs.org/ \
    && npm config set fetch-retries 5 \
    && npm config set fetch-retry-mintimeout 20000 \
    && npm config set fetch-retry-maxtimeout 120000

# Xóa các module GCP
RUN sed -i '/@google-cloud\/profiler/d' package.json \
    && sed -i '/@google-cloud\/debug-agent/d' package.json \
    && sed -i '/@google-cloud\/trace-agent/d' package.json

RUN npm install --omit=dev --no-audit

# Cài Seeker Agent
COPY seeker-node-agent.zip /tmp/agent.zip
RUN unzip -d /tmp/seeker /tmp/agent.zip \
    && npm install /tmp/seeker/*.tgz --save --no-audit --prefix /usr/src/app

# --- Final Stage ---
FROM node:20-alpine

ENV NODE_TLS_REJECT_UNAUTHORIZED=0
WORKDIR /usr/src/app

COPY --from=builder /usr/src/app/node_modules ./node_modules
COPY . .

# Tạo Mock Module 
RUN mkdir -p node_modules/@google-cloud/profiler \
    && echo "module.exports = { start: function() { console.log('Mock Profiler'); return {}; } };" > node_modules/@google-cloud/profiler/index.js \
    && mkdir -p node_modules/@google-cloud/debug-agent \
    && echo "module.exports = { start: function() { console.log('Mock Debugger'); return {}; } };" > node_modules/@google-cloud/debug-agent/index.js \
    && mkdir -p node_modules/@google-cloud/trace-agent \
    && echo "module.exports = { start: function() { console.log('Mock Tracer'); return {}; } };" > node_modules/@google-cloud/trace-agent/index.js

# [SEEKER] Cấu hình
ARG SEEKER_ACCESS_TOKEN
ENV SEEKER_ACCESS_TOKEN=$SEEKER_ACCESS_TOKEN
ENV SEEKER_SERVER_URL="http://192.168.12.190:8082"
ENV SEEKER_PROJECT_KEY="currencyservice"
ENV NODE_OPTIONS="--import @seeker/agent/index.mjs"

# [SỬA LỖI TẠI ĐÂY] Thêm biến môi trường PORT để server không bị undefined 
ENV PORT=7000

EXPOSE 7000
ENTRYPOINT [ "node", "server.js" ]
