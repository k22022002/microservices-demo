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
RUN npm install --only=production

# [SEEKER] Cài đặt Node.js Agent
COPY seeker-node-agent.zip /tmp/agent.zip
RUN unzip -d /tmp/seeker /tmp/agent.zip \
    && npm install /tmp/seeker/*.tgz --save --no-audit --prefix /usr/src/app

# --- Final Stage ---
FROM node:20-alpine

WORKDIR /usr/src/app

# Copy thư viện và code
COPY --from=builder /usr/src/app/node_modules ./node_modules
COPY . .

# [SEEKER] Cấu hình
ARG SEEKER_ACCESS_TOKEN
ENV SEEKER_ACCESS_TOKEN=$SEEKER_ACCESS_TOKEN
ENV SEEKER_SERVER_URL="http://192.168.12.190:8082"
ENV SEEKER_PROJECT_KEY="microservices-demo-nodejs"
ENV NODE_OPTIONS="--require @synopsys-sig/seeker"

EXPOSE 7000
ENTRYPOINT [ "node", "server.js" ]
