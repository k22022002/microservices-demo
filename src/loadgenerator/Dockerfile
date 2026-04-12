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
FROM python:3.14.2-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends g++ gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --prefix="/install" --no-cache-dir -r requirements.txt

# [SEEKER] Cài đặt Agent tại Builder (có prefix)
COPY seeker-python-agent.tar.gz /tmp/
RUN pip install --prefix="/install" --no-cache-dir /tmp/seeker-python-agent.tar.gz

# --- Final Stage ---
FROM python:3.14.2-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /loadgen

# Copy toàn bộ folder install
COPY --from=builder /install /usr/local
COPY locustfile.py .

# [SEEKER] Cấu hình
ARG SEEKER_ACCESS_TOKEN
ENV SEEKER_ACCESS_TOKEN=$SEEKER_ACCESS_TOKEN
ENV SEEKER_SERVER_URL="http://192.168.12.190:8082"
ENV SEEKER_PROJECT_KEY="microservices-demo-python"
ENV GEVENT_SUPPORT=True

ENTRYPOINT ["seeker-exec", "locust", "--host=http://${FRONTEND_ADDR}", "--headless", "-u", "${USERS:-10}", "-r", "${RATE:-1}"]
