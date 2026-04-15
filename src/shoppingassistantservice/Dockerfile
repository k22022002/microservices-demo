# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# --- Builder Stage ---
# Đổi xuống Python 3.11
FROM python:3.11-slim AS builder

RUN apt-get -qq update \
    && apt-get install -y --no-install-recommends g++ gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Vẫn giữ aiohttp đã fix ở bước trước
RUN pip install --no-cache-dir -r requirements.txt aiohttp

# [SEEKER] Cài đặt Agent tại Builder
COPY seeker-python-agent.tar.gz /tmp/
RUN pip install --no-cache-dir /tmp/seeker-python-agent.tar.gz

# --- Final Stage ---
# Đổi xuống Python 3.11
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /shoppingassistantservice

# [QUAN TRỌNG] Đổi đường dẫn copy từ python3.14 thành python3.11
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

COPY . .

# [SEEKER] Cấu hình
ARG SEEKER_ACCESS_TOKEN
ENV SEEKER_ACCESS_TOKEN=$SEEKER_ACCESS_TOKEN
ENV SEEKER_SERVER_URL="http://192.168.12.190:8082"
ENV SEEKER_PROJECT_KEY="microservices-demo-python"

# THÊM DÒNG NÀY (Thay "your-project-id" bằng ID thực tế hoặc một chuỗi bất kỳ để bypass lỗi)
ENV PROJECT_ID="your-project-id"
ENV REGION="us-central1"
ENV PORT="8080"
EXPOSE 8080

ENTRYPOINT ["seeker-exec", "python", "shoppingassistantservice.py"]
