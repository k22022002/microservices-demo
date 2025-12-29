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
FROM golang:1.22-alpine AS builder

# [FIX SSL] Chuyen Alpine repo sang HTTP
RUN sed -i 's/https/http/g' /etc/apk/repositories \
    && apk add --no-cache git

WORKDIR /src

# [SEEKER] Copy Tool
COPY seeker-agent-linux-amd64 /usr/local/bin/seeker-agent-build
RUN chmod +x /usr/local/bin/seeker-agent-build

COPY go.mod go.sum ./

# [FIX BUG - VERSION CONFLICT]
# 1. Hạ cấp version chính trong go.mod xuống 1.22
RUN sed -i 's/^go 1\.[0-9]\+/go 1.22/' go.mod

# 2. Xóa go.sum để reset ràng buộc phiên bản
RUN rm go.sum

# 3. Ép buộc hạ cấp các thư viện Google gây lỗi "requires go >= 1.24"
# Replace: cloud.google.com/go -> bản v0.110.0
RUN go mod edit -replace cloud.google.com/go=cloud.google.com/go@v0.110.0

# Replace: cloud.google.com/go/auth -> bản v0.13.0 (Tương thích Go 1.22)
RUN go mod edit -replace cloud.google.com/go/auth=cloud.google.com/go/auth@v0.13.0

# Replace: cloud.google.com/go/compute/metadata -> bản v0.2.3 (Fix trước để tránh lỗi tiếp theo)
RUN go mod edit -replace cloud.google.com/go/compute/metadata=cloud.google.com/go/compute/metadata@v0.2.3

# [FIX SSL] Cấu hình bỏ qua lỗi SSL và dùng Proxy HTTP
ENV GIT_SSL_NO_VERIFY=1
ENV GONOSUMDB=*
ENV GOINSECURE=*
# Dùng Proxy HTTP để tải lib nhanh và không check SSL
ENV GOPROXY=http://goproxy.cn,direct

# Lệnh này sẽ tự động tạo lại go.sum với các phiên bản đã replace ở trên
RUN go mod download

COPY . .

# [SEEKER] Build Wrapper
ARG SEEKER_URL="http://192.168.12.190:8082"
ARG SEEKER_PROJECT="microservices-demo"

ENV CGO_ENABLED=0 

RUN export SEEKER_SERVER_URL=$SEEKER_URL \
    && export SEEKER_PROJECT_KEY=$SEEKER_PROJECT \
    && /usr/local/bin/seeker-agent-build go build -o /go/bin/frontend .

# --- Final Stage ---
FROM alpine:latest

# [FIX SSL] Chuyen Alpine repo sang HTTP
RUN sed -i 's/https/http/g' /etc/apk/repositories \
    && apk add --no-cache ca-certificates

WORKDIR /src
COPY --from=builder /go/bin/frontend /src/server
COPY ./templates ./templates
COPY ./static ./static

# [SEEKER] Runtime Config
ENV SEEKER_SERVER_URL="http://192.168.12.190:8082"
ENV SEEKER_PROJECT_KEY="microservices-demo"
ENV GOTRACEBACK=single

EXPOSE 8080
ENTRYPOINT ["/src/server"]
