# Copyright 2021 Google LLC
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

# https://mcr.microsoft.com/product/dotnet/sdk
# --- Builder Stage ---
FROM --platform=$BUILDPLATFORM mcr.microsoft.com/dotnet/sdk:10.0.100-noble AS builder
ARG TARGETARCH
WORKDIR /app

RUN apt-get update && apt-get install -y unzip

# Tải và Restore Code
COPY cartservice.csproj .
RUN dotnet restore cartservice.csproj -a $TARGETARCH
COPY . .

# Build dự án
RUN dotnet publish cartservice.csproj \
    -p:PublishSingleFile=true -a $TARGETARCH \
    --self-contained true -p:PublishTrimmed=true \
    -p:TrimMode=full -c release -o /cartservice

# [SEEKER] Chuẩn bị .NET Agent
COPY seeker-dotnet-agent.zip /tmp/
RUN unzip /tmp/seeker-dotnet-agent.zip -d /seeker-agent

# --- Final Stage ---
FROM mcr.microsoft.com/dotnet/runtime-deps:10.0.0-noble-chiseled

WORKDIR /app
COPY --from=builder /cartservice .
COPY --from=builder /seeker-agent /seeker-agent

# [SEEKER] Cấu hình CoreCLR Profiler
ARG SEEKER_ACCESS_TOKEN
ENV SEEKER_ACCESS_TOKEN=$SEEKER_ACCESS_TOKEN
ENV SEEKER_SERVER_URL="http://192.168.12.190:8082"
ENV SEEKER_PROJECT_KEY="microservices-demo-dotnet"
ENV CORECLR_ENABLE_PROFILING=1
ENV CORECLR_PROFILER="{83CC9B47-19DE-45CA-9E39-20412BECEBA0}"
ENV CORECLR_PROFILER_PATH="/seeker-agent/libcoreclr-profiler.so"

EXPOSE 7070
ENV DOTNET_EnableDiagnostics=0 \
    ASPNETCORE_HTTP_PORTS=7070
USER 1000
ENTRYPOINT ["/app/cartservice"]
