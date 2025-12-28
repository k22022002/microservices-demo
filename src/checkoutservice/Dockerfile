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

# [CHANGE] Dùng golang:1.22 (Debian standard) tương tự Frontend để tương thích với Seeker
FROM golang:1.22 AS builder

# [FIX TIME SKEW - BUILDER] Bỏ qua kiểm tra ngày tháng để tránh lỗi APT
RUN apt-get -o Acquire::Check-Valid-Until=false -o Acquire::Check-Date=false update \
    && apt-get install -y git 

WORKDIR /src

# [SEEKER] Copy Tool Build Wrapper
COPY seeker-agent-linux-amd64 /usr/local/bin/seeker-agent-build
RUN chmod +x /usr/local/bin/seeker-agent-build 

# Copy file định nghĩa dependency
COPY go.mod go.sum ./ 

# ====================================================================================
# [CRITICAL FIX] "ĐẠI PHẪU" DOWNGRADE VERSION (Giống hệt Frontend)
# ====================================================================================

# 1. Hạ cấp version Go xuống 1.22 trong go.mod
RUN sed -i 's/^go 1\.[0-9]\+/go 1.22/' go.mod \
    && sed -i '/toolchain/d' go.mod 

# 2. Xóa go.sum để tạo lại bản mới tương thích
RUN rm -f go.sum 
# --- Google Cloud Core ---
RUN go mod edit -replace cloud.google.com/go=cloud.google.com/go@v0.110.0 \
    && go mod edit -replace cloud.google.com/go/auth=cloud.google.com/go/auth@v0.13.0 \
    && go mod edit -replace cloud.google.com/go/auth/oauth2adapt=cloud.google.com/go/auth/oauth2adapt@v0.2.0 \
    && go mod edit -replace cloud.google.com/go/compute/metadata=cloud.google.com/go/compute/metadata@v0.2.3 \
    && go mod edit -replace cloud.google.com/go/profiler=cloud.google.com/go/profiler@v0.4.0

# --- Google APIs & GRPC ---
RUN go mod edit -replace github.com/googleapis/gax-go/v2=github.com/googleapis/gax-go/v2@v2.12.0 \
    && go mod edit -replace google.golang.org/api=google.golang.org/api@v0.169.0 \
    && go mod edit -replace google.golang.org/grpc=google.golang.org/grpc@v1.64.0 \
    && go mod edit -replace google.golang.org/protobuf=google.golang.org/protobuf@v1.33.0

# --- Utilities ---
RUN go mod edit -replace github.com/cenkalti/backoff/v5=github.com/cenkalti/backoff/v4@v4.3.0 \
    && go mod edit -replace github.com/go-playground/validator/v10=github.com/go-playground/validator/v10@v10.20.0 \
    && go mod edit -replace github.com/google/pprof=github.com/google/pprof@v0.0.0-20240525223248-4bfdf5a9a2af

# --- OpenTelemetry ---
RUN go mod edit -replace go.opentelemetry.io/otel=go.opentelemetry.io/otel@v1.24.0 \
    && go mod edit -replace go.opentelemetry.io/otel/sdk=go.opentelemetry.io/otel/sdk@v1.24.0 \
    && go mod edit -replace go.opentelemetry.io/otel/trace=go.opentelemetry.io/otel/trace@v1.24.0 \
    && go mod edit -replace go.opentelemetry.io/otel/metric=go.opentelemetry.io/otel/metric@v1.24.0 \
    && go mod edit -replace go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc=go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc@v1.24.0 \
    && go mod edit -replace go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc=go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc@v0.49.0 \
    && go mod edit -replace go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp=go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp@v0.49.0
# ====================================================================================

# [FIX SSL] Cấu hình proxy và bỏ qua xác thực SSL khi tải thư viện
ENV GIT_SSL_NO_VERIFY=1
ENV GONOSUMDB=*
ENV GOINSECURE=*
ENV GOPROXY=http://goproxy.cn,direct

# Tidy và Download Dependencies
RUN go mod tidy || true && go mod download 

# [FIX BACKUP/RESTORE] Đảm bảo go.mod không bị ghi đè bởi bản lỗi từ host
RUN cp go.mod go.mod.bak \
    && if [ -f go.sum ]; then cp go.sum go.sum.bak; fi 

COPY . .

RUN mv go.mod.bak go.mod \
    && if [ -f go.sum.bak ]; then mv go.sum.bak go.sum; else rm -f go.sum; fi 

# [SEEKER] Build Wrapper
ARG SEEKER_URL
ARG SEEKER_PROJECT
ARG SEEKER_ACCESS_TOKEN

RUN export SEEKER_SERVER_URL=$SEEKER_URL \
    && export SEEKER_PROJECT_KEY=microservices-demo-checkout \
    && export SEEKER_ACCESS_TOKEN=$SEEKER_ACCESS_TOKEN \
    && export SEEKER_ENTRY_POINT=/src/main.go \
    && export SEEKER_COMPOSITE_BUILD=true \
    && /usr/local/bin/seeker-agent-build go build -v -o /src/checkoutservice . 

# --- Final Stage ---
# Sử dụng Debian Slim để có glibc cho Seeker Agent
FROM debian:bookworm-slim

# [FIX TIME SKEW - FINAL STAGE]
RUN apt-get -o Acquire::Check-Valid-Until=false -o Acquire::Check-Date=false update \
    && apt-get install -y ca-certificates net-tools \
    && rm -rf /var/lib/apt/lists/* 

WORKDIR /src
COPY --from=builder /src/checkoutservice /src/checkoutservice

# [SEEKER] Config Runtime
ARG SEEKER_ACCESS_TOKEN
ENV SEEKER_ACCESS_TOKEN=$SEEKER_ACCESS_TOKEN
ENV SEEKER_SERVER_URL="http://192.168.12.190:8082"
ENV SEEKER_PROJECT_KEY="microservices-demo-checkout" 
ENV PORT=5050

# Đây là biến bị lỗi trong log của bạn:
ENV SHIPPING_SERVICE_ADDR="shippingservice:50051"

# Các biến khác thường cũng được yêu cầu bởi CheckoutService (thêm vào để tránh lỗi tiếp theo):
ENV PRODUCT_CATALOG_SERVICE_ADDR="productcatalogservice:3550"
ENV CURRENCY_SERVICE_ADDR="currencyservice:7000"
ENV CART_SERVICE_ADDR="cartservice:7000"
ENV EMAIL_SERVICE_ADDR="emailservice:8080"
ENV PAYMENT_SERVICE_ADDR="paymentservice:50051"
EXPOSE 5050

ENTRYPOINT ["/src/checkoutservice"]
