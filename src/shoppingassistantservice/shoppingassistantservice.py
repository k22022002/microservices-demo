#!/usr/bin/python
#
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

#!/usr/bin/python
import os
from urllib.parse import unquote
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from flask import Flask, request

# === ĐÃ VÔ HIỆU HÓA DB ĐỂ TEST SEEKER ===
# from google.cloud import secretmanager_v1
# from langchain_google_alloydb_pg import AlloyDBEngine, AlloyDBVectorStore

def create_app():
    app = Flask(__name__)

    @app.route("/", methods=['POST'])
    def talkToGemini():
        print("Beginning Mocked RAG call")
        prompt = request.json.get('message', '')
        prompt = unquote(prompt)

        # Trả về một phản hồi giả lập đơn giản ngay lập tức để test luồng HTTP
        # Seeker vẫn sẽ ghi nhận được việc dữ liệu đầu vào (prompt) đi vào ứng dụng (Source)
        # và được trả ra ngoài (Sink).
        design_response = f"Đây là phản hồi giả lập để test Seeker Agent. Bạn vừa gửi yêu cầu: {prompt}"
        
        data = {'content': design_response}
        return data

    return app

if __name__ == "__main__":
    # Create an instance of flask server when called directly
    app = create_app()
    app.run(host='0.0.0.0', port=8080)
