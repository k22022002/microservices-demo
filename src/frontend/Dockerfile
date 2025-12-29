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

# [FIX LOI SSL] Chuyen repo sang HTTP
RUN sed -i 's/https/http/g' /etc/apk/repositories \
    && apk add --no-cache git

WORKDIR /src

# [SEEKER] Copy Tool
COPY seeker-agent-linux-amd64 /usr/local/bin/seeker-agent-build
RUN chmod +x /usr/local/bin/seeker-agent-build

COPY go.mod go.sum ./
# [FIX SSL] Tat check sum database
ENV GONOSUMDB=*
# [FIX SSL] Cho phep insecure (http) khi go get
ENV GOINSECURE=* RUN go mod download

COPY . .

# [SEEKER] Build
ARG SEEKER_URL="http://192.168.12.190:8082"
ARG SEEKER_PROJECT="microservices-demo"

ENV CGO_ENABLED=0 

RUN export SEEKER_SERVER_URL=$SEEKER_URL \
    && export SEEKER_PROJECT_KEY=$SEEKER_PROJECT \
    && /usr/local/bin/seeker-agent-build go build -o /go/bin/frontend .

# --- Final Stage ---
FROM alpine:latest
# [FIX SSL] Chuyen repo sang HTTP
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
