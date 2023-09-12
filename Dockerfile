# Copyright 2023 Louis Wendler
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM python:3.11-slim-bullseye AS compile-image
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

WORKDIR /app

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY README.md .
COPY setup.py .
COPY src/ src/
RUN python3 -m pip install -e .

FROM python:3.11-slim-bullseye AS build-image

WORKDIR /app

COPY --from=compile-image /app/src /app/src
COPY --from=compile-image /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"
CMD ["python3", "src/gradio_chat/app.py", "--server_name", "0.0.0.0", "--cache", "/tmp/.cache", "--log_dir", "/tmp/.logs"]