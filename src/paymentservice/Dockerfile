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

# [QUAN TRỌNG] 1. Cài đặt Python và công cụ biên dịch (để build pprof và dependencies)
RUN sed -i 's/https/http/g' /etc/apk/repositories \
    && apk add --no-cache python3 make g++ unzip tar

RUN npm config set strict-ssl false
ENV NODE_TLS_REJECT_UNAUTHORIZED=0

WORKDIR /usr/src/app
COPY package*.json ./

# Xóa bớt google-cloud-profiler nếu không cần thiết
RUN sed -i '/@google-cloud\/profiler/d' package.json \
    && sed -i '/@google-cloud\/debug-agent/d' package.json

# 2. Cài đặt App Dependencies (Production only)
RUN npm install --only=production --no-audit

# 3. Cài đặt Seeker Agent (Phương pháp chuẩn: Install file .tgz)
COPY seeker-node-agent.zip /tmp/seeker-node-agent.zip
RUN unzip -d /tmp/seeker /tmp/seeker-node-agent.zip

# [FIX LOI 404] Thay vì giải nén, ta cài thẳng file .tgz vào node_modules
# - "--prefix /usr/src/app": Sửa lỗi "required argument --prefix" bạn gặp lúc đầu
# - "--no-save": Không sửa file package.json
RUN find /tmp/seeker -name "seeker-agent.tgz" -exec npm install {} --prefix /usr/src/app --no-save --no-audit \;

# --- Final Stage ---
FROM node:20-alpine
ENV NODE_TLS_REJECT_UNAUTHORIZED=0
WORKDIR /usr/src/app

# Copy node_modules (Lúc này Seeker Agent đã nằm gọn trong node_modules/@synopsys-sig/seeker)
COPY --from=builder /usr/src/app/node_modules ./node_modules

COPY . .

# [SEEKER] Config
ARG SEEKER_ACCESS_TOKEN
ENV SEEKER_ACCESS_TOKEN=$SEEKER_ACCESS_TOKEN
ENV SEEKER_SERVER_URL="http://192.168.12.190:8082"
ENV SEEKER_PROJECT_KEY="microservices-demo"

# [FIX PATH] Trỏ vào agent nằm trong node_modules chuẩn
# Lưu ý: Đường dẫn này khác với cách giải nén thủ công
ENV NODE_OPTIONS="--import ./node_modules/@synopsys-sig/seeker/agent/index.mjs"

EXPOSE 50051
ENTRYPOINT [ "node", "index.js" ]
