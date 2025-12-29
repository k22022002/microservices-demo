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
# --- Builder Stage ---
FROM node:20-alpine AS builder

# [FIX SSL/TIME] Chuyen repo sang HTTP de tranh loi chung chi
RUN sed -i 's/https/http/g' /etc/apk/repositories

RUN apk add --update --no-cache python3 make g++ unzip

WORKDIR /usr/src/app

COPY package*.json ./

# [SEEKER] 1. Copy file zip
COPY seeker-node-agent.zip /tmp/seeker-node-agent.zip

# [SEEKER] 2. Cai dat Agent
RUN mkdir -p seeker \
    && unzip -d seeker /tmp/seeker-node-agent.zip \
    && npm install ./seeker/seeker-agent.tgz --prefix seeker --save

# 3. Install App Deps
RUN npm install --only=production

# --- Final Stage ---
FROM node:20-alpine

WORKDIR /usr/src/app

COPY --from=builder /usr/src/app/node_modules ./node_modules
COPY --from=builder /usr/src/app/seeker ./seeker

COPY . .

# [SEEKER] 3. Config
ENV SEEKER_SERVER_URL="http://192.168.12.190:8082"
ENV SEEKER_PROJECT_KEY="microservices-demo"
# Node 20 dung --import
ENV NODE_OPTIONS="--import ./seeker/node_modules/@synopsys-sig/seeker/agent/index.mjs"

EXPOSE 50051
ENTRYPOINT [ "node", "index.js" ]
