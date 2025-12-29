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

# [FIX SSL] Chuyen Alpine repo sang HTTP
RUN sed -i 's/https/http/g' /etc/apk/repositories \
    && apk add --update --no-cache python3 make g++ unzip

# [FIX SSL] Tat kiem tra SSL cho NPM
RUN npm config set strict-ssl false
ENV NODE_TLS_REJECT_UNAUTHORIZED=0

WORKDIR /usr/src/app

COPY package*.json ./

# [FIX BUG - QUAN TRỌNG]
# 1. Xóa dòng chứa "pprof" trong package.json
RUN sed -i '/"pprof":/d' package.json

# 2. Xóa luôn package-lock.json để tránh npm tự động tải lại pprof từ file lock cũ
RUN rm -f package-lock.json

# [SEEKER] Copy & Install Agent
COPY seeker-node-agent.zip /tmp/seeker-node-agent.zip

RUN mkdir -p seeker \
    && unzip -d seeker /tmp/seeker-node-agent.zip \
    && npm install ./seeker/seeker-agent.tgz --prefix seeker --save

# Install App Deps
# Lưu ý: Thêm --no-optional để bỏ qua các gói phụ
RUN npm install --only=production --no-optional

# --- Final Stage ---
FROM node:20-alpine

# [FIX SSL] Tat SSL Runtime
ENV NODE_TLS_REJECT_UNAUTHORIZED=0

WORKDIR /usr/src/app

COPY --from=builder /usr/src/app/node_modules ./node_modules
COPY --from=builder /usr/src/app/seeker ./seeker

COPY . .

# [SEEKER] Config
ENV SEEKER_SERVER_URL="http://192.168.12.190:8082"
ENV SEEKER_PROJECT_KEY="microservices-demo"
ENV NODE_OPTIONS="--import ./seeker/node_modules/@synopsys-sig/seeker/agent/index.mjs"

EXPOSE 50051
ENTRYPOINT [ "node", "index.js" ]
