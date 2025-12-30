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

# [CHANGE] Dùng golang:1.22 (Debian) thay vì alpine để tương thích 100% với Seeker Agent (glibc)
# Điều này sẽ khắc phục lỗi treo mà không cần cài thêm thư viện tương thích.
FROM golang:1.22 AS builder

WORKDIR /src

# [SEEKER] Copy Tool
COPY seeker-agent-linux-amd64 /usr/local/bin/seeker-agent-build
RUN chmod +x /usr/local/bin/seeker-agent-build

# Copy file định nghĩa dependency
COPY go.mod go.sum ./

# ====================================================================================
# [CRITICAL FIX] DOWNGRADE VERSION (Logic cũ vẫn cần thiết)
# ====================================================================================

# 1. Sửa header go.mod: Hạ từ 1.25 xuống 1.22 và xóa toolchain
RUN sed -i 's/^go 1\.[0-9]\+/go 1.22/' go.mod \
    && sed -i '/toolchain/d' go.mod

# 2. Xóa go.sum cũ
RUN rm -f go.sum

# 3. REPLACE TOÀN DIỆN:
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

# [FIX SSL] Cấu hình proxy và SSL bypass
ENV GIT_SSL_NO_VERIFY=1
ENV GONOSUMDB=*
ENV GOINSECURE=*
ENV GOPROXY=http://goproxy.cn,direct

# Tidy và Download Dependencies
# Lưu ý: Debian có sẵn git, không cần cài thêm
RUN go mod tidy || true && go mod download

# [FIX BACKUP] Backup go.mod
RUN cp go.mod go.mod.bak \
    && if [ -f go.sum ]; then cp go.sum go.sum.bak; else echo "No go.sum to backup"; fi

# Copy source code (Ghi đè go.mod bằng bản lỗi 1.25 từ host)
COPY . .

# [FIX RESTORE] Khôi phục go.mod chuẩn
RUN mv go.mod.bak go.mod \
    && if [ -f go.sum.bak ]; then mv go.sum.bak go.sum; else rm -f go.sum; fi

# [SEEKER] Build Wrapper
ARG SEEKER_URL="http://192.168.12.190:8082"
ARG SEEKER_PROJECT="microservices-demo"

# CGO_ENABLED=0 là bắt buộc để build file tĩnh (chạy được trên Alpine ở bước sau)
ENV CGO_ENABLED=0 

# [FIX HANG]
# 1. Dùng Debian base nên Seeker Agent chạy native, không lo treo do musl.
# 2. Vẫn giữ SEEKER_COMPOSITE_BUILD=true để tránh treo do mạng.
RUN export SEEKER_SERVER_URL=$SEEKER_URL \
    && export SEEKER_PROJECT_KEY=$SEEKER_PROJECT \
    && export SEEKER_ENTRY_POINT=/src/main.go \
    && export SEEKER_COMPOSITE_BUILD=true \
    && /usr/local/bin/seeker-agent-build go build -v -o /go/bin/frontend .

# --- Final Stage ---
# Vẫn dùng Alpine để runtime nhẹ
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
