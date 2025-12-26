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

# [QUAN TRỌNG] 1. Cài đặt App Dependencies TRƯỚC
# Để tránh việc npm install sau này xóa mất Seeker Agent
RUN npm install --only=production --no-audit

# [SEEKER] 2. Cài đặt Agent SAU
COPY seeker-node-agent.zip /tmp/seeker-node-agent.zip
RUN unzip -d /tmp/seeker /tmp/seeker-node-agent.zip

# Tìm file tgz và cài đặt thẳng vào node_modules hiện tại
# Dùng flag --no-save để không sửa package.json (tránh xung đột lockfile)
RUN find /tmp/seeker -name "seeker-agent.tgz" -exec npm install {} --prefix /usr/src/app --no-save --no-audit \;

# --- Final Stage ---
FROM node:20-alpine
ENV NODE_TLS_REJECT_UNAUTHORIZED=0
WORKDIR /usr/src/app

# Copy node_modules (đã bao gồm Seeker Agent)
COPY --from=builder /usr/src/app/node_modules ./node_modules

COPY . .

# [SEEKER] Config
ARG SEEKER_ACCESS_TOKEN
ENV SEEKER_ACCESS_TOKEN=$SEEKER_ACCESS_TOKEN
ENV SEEKER_SERVER_URL="http://192.168.12.190:8082"
ENV SEEKER_PROJECT_KEY="microservices-demo"

# [FIX PATH] Import module Seeker
ENV NODE_OPTIONS="--import @synopsys-sig/seeker/agent/index.mjs"

EXPOSE 50051
ENTRYPOINT [ "node", "index.js" ]
