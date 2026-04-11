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
FROM golang:1.25.6-bookworm AS builder
ARG TARGETOS
ARG TARGETARCH

WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .

# [SEEKER] Cài đặt Go Agent Build Wrapper
COPY seeker-agent-linux-amd64 /usr/local/bin/seeker-agent-build
RUN chmod +x /usr/local/bin/seeker-agent-build

# [SEEKER] Build Code
ARG SEEKER_URL="http://192.168.12.190:8082"
ARG SEEKER_ACCESS_TOKEN
ARG SKAFFOLD_GO_GCFLAGS

RUN export SEEKER_SERVER_URL=$SEEKER_URL \
    && export SEEKER_PROJECT_KEY="microservices-demo-go" \
    && export SEEKER_ACCESS_TOKEN=$SEEKER_ACCESS_TOKEN \
    && export SEEKER_ENTRY_POINT=/src/main.go \
    && export SEEKER_COMPOSITE_BUILD=true \
    && GOOS=${TARGETOS} GOARCH=${TARGETARCH} CGO_ENABLED=0 \
       /usr/local/bin/seeker-agent-build go build -ldflags="-s -w" -gcflags="${SKAFFOLD_GO_GCFLAGS}" -o /productcatalogservice .

# --- Final Stage ---
FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*

WORKDIR /src
COPY --from=builder /productcatalogservice ./server
COPY products.json .

# [SEEKER] Cấu hình Runtime
ARG SEEKER_ACCESS_TOKEN
ENV SEEKER_ACCESS_TOKEN=$SEEKER_ACCESS_TOKEN
ENV SEEKER_SERVER_URL="http://192.168.12.190:8082"
ENV SEEKER_PROJECT_KEY="microservices-demo-go"
ENV SEEKER_AGENT_NAME="productcatalog-service"

ENV GOTRACEBACK=single
EXPOSE 3550
ENTRYPOINT ["/src/server"]
