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
FROM golang:1.22 AS builder

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
ARG SEEKER_ACCESS_TOKEN

RUN export SEEKER_SERVER_URL=$SEEKER_URL \
    && export SEEKER_PROJECT_KEY="microservices-demo-checkout" \
    && export SEEKER_ACCESS_TOKEN=$SEEKER_ACCESS_TOKEN \
    && export SEEKER_ENTRY_POINT=/src/main.go \
    && export SEEKER_COMPOSITE_BUILD=true \
    && /usr/local/bin/seeker-agent-build go build -v -o /src/checkoutservice .

# --- Final Stage ---
FROM debian:bookworm-slim

RUN apt-get update \
    && apt-get install -y ca-certificates net-tools \
    && rm -rf /var/lib/apt/lists/* WORKDIR /src
COPY --from=builder /src/checkoutservice /src/checkoutservice

# Cấu hình Runtime Seeker
ARG SEEKER_ACCESS_TOKEN
ENV SEEKER_ACCESS_TOKEN=$SEEKER_ACCESS_TOKEN
ENV SEEKER_SERVER_URL="http://192.168.12.190:8082"
ENV SEEKER_PROJECT_KEY="microservices-demo-checkout" 
ENV PORT=5050

ENV SHIPPING_SERVICE_ADDR="shippingservice:50051"
ENV PRODUCT_CATALOG_SERVICE_ADDR="productcatalogservice:3550"
ENV CURRENCY_SERVICE_ADDR="currencyservice:7000"
ENV CART_SERVICE_ADDR="cartservice:7070"
ENV EMAIL_SERVICE_ADDR="emailservice:8080"
ENV PAYMENT_SERVICE_ADDR="paymentservice:50051"

EXPOSE 5050
ENTRYPOINT ["/src/checkoutservice"]
