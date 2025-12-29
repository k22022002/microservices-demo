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
FROM node:20.20.0-alpine@sha256:3960ed74dfe320a67bf8da9555b6bade25ebda2b22b6081d2f60fd7d5d430e9c AS builder

RUN apk add --update --no-cache python3 make g++ unzip

WORKDIR /usr/src/app

COPY package*.json ./

# [SEEKER] 1. Copy file zip Agent (được tải bởi Jenkins)
COPY seeker-node-agent.zip /tmp/seeker-node-agent.zip

# [SEEKER] 2. Giải nén và cài đặt Agent vào thư mục 'seeker'
RUN mkdir -p seeker \
    && unzip -d seeker /tmp/seeker-node-agent.zip \
    && npm install ./seeker/seeker-agent.tgz --prefix seeker --save

# 3. Cài đặt dependencies của app
RUN npm install --only=production

# --- Final Stage ---
FROM alpine:3.23.2@sha256:865b95f46d98cf867a156fe4a135ad3fe50d2056aa3f25ed31662dff6da4eb62

RUN apk add --no-cache nodejs

WORKDIR /usr/src/app

# Copy dependencies (bao gồm cả seeker đã cài ở trên)
COPY --from=builder /usr/src/app/node_modules ./node_modules
# Copy folder seeker riêng (chứa cấu hình agent)
COPY --from=builder /usr/src/app/seeker ./seeker

COPY . .

# [SEEKER] 3. Cấu hình biến môi trường
ENV SEEKER_SERVER_URL="http://192.168.12.190:8082"
ENV SEEKER_PROJECT_KEY="microservices-demo"
# Node 20 hỗ trợ ESM loader, dùng --import như hướng dẫn trong hình của bạn
ENV NODE_OPTIONS="--import ./seeker/node_modules/@synopsys-sig/seeker/agent/index.mjs"

EXPOSE 50051

ENTRYPOINT [ "node", "index.js" ]
