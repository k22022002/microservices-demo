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
# --- Builder Stage ---
# Đã xóa --platform=$BUILDPLATFORM
FROM mcr.microsoft.com/dotnet/sdk:10.0.100-noble AS builder
WORKDIR /app

RUN apt-get update && apt-get install -y unzip

# Tải và Restore Code (Đã xóa -a $TARGETARCH)
COPY cartservice.csproj .
RUN dotnet restore cartservice.csproj
COPY . .

# Build dự án cho môi trường IAST (Tắt Trim và SingleFile)
RUN dotnet publish cartservice.csproj \
    --self-contained true \
    -c release \
    -o /cartservice
# [SEEKER] Chuẩn bị .NET Agent
COPY seeker-dotnet-agent.zip /tmp/
RUN unzip /tmp/seeker-dotnet-agent.zip -d /seeker-agent && \
    chmod -R 755 /seeker-agent
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

# SỬA LẠI ĐÚNG GUID CỦA SEEKER
ENV CORECLR_PROFILER="{C7AD49B3-093B-4AB1-A241-1E4365DD8901}"

# SỬA LẠI ĐÚNG ĐƯỜNG DẪN FILE .so (Thường nằm trong thư mục x64)
ENV CORECLR_PROFILER_PATH="/seeker-agent/x64/Agent.Profiler-Dnc.so"
EXPOSE 7070
ENV DOTNET_EnableDiagnostics=1 \
    ASPNETCORE_HTTP_PORTS=7070
USER 1000
ENTRYPOINT ["/app/cartservice"]
