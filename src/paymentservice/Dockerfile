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

# [QUAN TRỌNG] Tắt kiểm tra SSL cho Node.js và NPM
ENV NODE_TLS_REJECT_UNAUTHORIZED=0
RUN npm config set strict-ssl false

RUN apk add --update --no-cache python3 make g++ unzip

WORKDIR /usr/src/app

COPY package*.json ./

# [SEEKER] Copy Agent
COPY seeker-node-agent.zip /tmp/seeker-node-agent.zip

# [SEEKER] Cài Agent
RUN mkdir -p seeker \
    && unzip -d seeker /tmp/seeker-node-agent.zip \
    && npm install ./seeker/seeker-agent.tgz --prefix seeker --save

# Install Dependencies
RUN npm install --only=production

# --- Final Stage ---
FROM node:20-alpine

# [QUAN TRỌNG] Tắt SSL Runtime (để Agent gửi dữ liệu về Seeker Server không bị lỗi)
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
