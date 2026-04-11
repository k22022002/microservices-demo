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

# [CHANGE] Dùng golang:1.22 (Debian standard) thay vì alpine để tương thích 100% với Seeker Agent (glibc)
# Đổi dòng này thành 1.25.6-bookworm
FROM golang:1.25.6-bookworm AS builder

RUN apt-get update && apt-get install -y git

WORKDIR /src

# Cài đặt Seeker Build Wrapper
COPY seeker-agent-linux-amd64 /usr/local/bin/seeker-agent-build
RUN chmod +x /usr/local/bin/seeker-agent-build

COPY go.mod go.sum ./
RUN go mod download

COPY . .

# Build bằng Seeker Wrapper
ARG SEEKER_URL="http://192.168.12.190:8082"
ARG SEEKER_PROJECT_KEY="microservices-demo-go"
ARG SEEKER_ACCESS_TOKEN

RUN export SEEKER_SERVER_URL=$SEEKER_URL \
    && export SEEKER_PROJECT_KEY=$SEEKER_PROJECT_KEY \
    && export SEEKER_ACCESS_TOKEN=$SEEKER_ACCESS_TOKEN \
    && export SEEKER_ENTRY_POINT=/src/main.go \
    && export SEEKER_COMPOSITE_BUILD=true \
    && /usr/local/bin/seeker-agent-build go build -a -v -o /go/bin/frontend .

# --- Final Stage ---
FROM debian:bookworm-slim

RUN apt-get update \
    && apt-get install -y ca-certificates net-tools \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src
COPY --from=builder /go/bin/frontend /src/server
COPY ./templates ./templates
COPY ./static ./static

# Cấu hình Runtime Seeker
ARG SEEKER_ACCESS_TOKEN
ENV SEEKER_ACCESS_TOKEN=$SEEKER_ACCESS_TOKEN
ENV SEEKER_SERVER_URL="http://192.168.12.190:8082"
ENV SEEKER_PROJECT_KEY="microservices-demo-go"
ENV SEEKER_AGENT_NAME="frontend-service"

# Biến môi trường App
ENV PRODUCT_CATALOG_SERVICE_ADDR="productcatalogservice:3550"
ENV CURRENCY_SERVICE_ADDR="currencyservice:7000"
ENV CART_SERVICE_ADDR="cartservice:7070"
ENV RECOMMENDATION_SERVICE_ADDR="recommendationservice:8080"
ENV SHIPPING_SERVICE_ADDR="shippingservice:50051"
ENV CHECKOUT_SERVICE_ADDR="checkoutservice:5050"
ENV AD_SERVICE_ADDR="adservice:9555"
ENV SHOPPING_ASSISTANT_SERVICE_ADDR="shopping-assistant:8080"

EXPOSE 8080
ENTRYPOINT ["/src/server"]
