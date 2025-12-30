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

# Copy file định nghĩa dependency
COPY go.mod go.sum ./

# ====================================================================================
# [CRITICAL FIX] "ĐẠI PHẪU" DOWNGRADE VERSION
# Mục tiêu: Ép toàn bộ dự án về chuẩn Go 1.22 (thay vì Go 1.25 như trong code gốc)
# ====================================================================================

# 1. Sửa header go.mod: Hạ từ 1.25 xuống 1.22 và xóa toolchain
RUN sed -i 's/^go 1\.[0-9]\+/go 1.22/' go.mod \
    && sed -i '/toolchain/d' go.mod

# 2. Xóa go.sum cũ để tránh xung đột checksum
RUN rm go.sum

# 3. REPLACE TOÀN DIỆN: Ép dùng phiên bản cũ tương thích Go 1.22
# --- Nhóm 1: Google Cloud Core (Gây lỗi auth, metadata, profiler) ---
RUN go mod edit -replace cloud.google.com/go=cloud.google.com/go@v0.110.0 \
    && go mod edit -replace cloud.google.com/go/auth=cloud.google.com/go/auth@v0.13.0 \
    && go mod edit -replace cloud.google.com/go/auth/oauth2adapt=cloud.google.com/go/auth/oauth2adapt@v0.2.0 \
    && go mod edit -replace cloud.google.com/go/compute/metadata=cloud.google.com/go/compute/metadata@v0.2.3 \
    && go mod edit -replace cloud.google.com/go/profiler=cloud.google.com/go/profiler@v0.4.0

# --- Nhóm 2: Google APIs & GRPC (Gây lỗi backoff/v5, requires go 1.23) ---
RUN go mod edit -replace github.com/googleapis/gax-go/v2=github.com/googleapis/gax-go/v2@v2.12.0 \
    && go mod edit -replace google.golang.org/api=google.golang.org/api@v0.169.0 \
    && go mod edit -replace google.golang.org/grpc=google.golang.org/grpc@v1.64.0 \
    && go mod edit -replace google.golang.org/protobuf=google.golang.org/protobuf@v1.33.0

# --- Nhóm 3: Utilities (Gây lỗi requires go 1.24) ---
# Backoff: Thay v5 bằng v4
RUN go mod edit -replace github.com/cenkalti/backoff/v5=github.com/cenkalti/backoff/v4@v4.3.0
# Validator: Hạ về v10.20.0
RUN go mod edit -replace github.com/go-playground/validator/v10=github.com/go-playground/validator/v10@v10.20.0
# Pprof: Hạ về bản tháng 5/2024
RUN go mod edit -replace github.com/google/pprof=github.com/google/pprof@v0.0.0-20240525223248-4bfdf5a9a2af

# --- Nhóm 4: OpenTelemetry (Hạ từ v1.39 xuống v1.24 để khớp với GRPC cũ) ---
RUN go mod edit -replace go.opentelemetry.io/otel=go.opentelemetry.io/otel@v1.24.0 \
    && go mod edit -replace go.opentelemetry.io/otel/sdk=go.opentelemetry.io/otel/sdk@v1.24.0 \
    && go mod edit -replace go.opentelemetry.io/otel/trace=go.opentelemetry.io/otel/trace@v1.24.0 \
    && go mod edit -replace go.opentelemetry.io/otel/metric=go.opentelemetry.io/otel/metric@v1.24.0 \
    && go mod edit -replace go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc=go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc@v1.24.0 \
    && go mod edit -replace go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc=go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc@v0.49.0 \
    && go mod edit -replace go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp=go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp@v0.49.0

# ====================================================================================

# [FIX SSL] Cấu hình bỏ qua lỗi SSL và dùng Proxy HTTP
ENV GIT_SSL_NO_VERIFY=1
ENV GONOSUMDB=*
ENV GOINSECURE=*
# Dùng Proxy HTTP để tải lib nhanh và không check SSL
ENV GOPROXY=http://goproxy.cn,direct

# Chạy tidy để dọn dẹp dependency graph sau khi replace
RUN go mod tidy

# Download dependencies
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
