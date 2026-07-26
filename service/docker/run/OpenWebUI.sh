#!/bin/bash

mkdir -p ${HOME}/Docker/OpenWebUI/data

docker run -d \
  -p 8080:8080 \
  -e WEBUI_SECRET_KEY=openstreetmap \
  -v ${HOME}/Docker/OpenWebUI/data:/app/backend/data \
  -e TZ=Asia/Shanghai \
  --restart unless-stopped \
  --name OpenWebUI \
  dyrnq/open-webui

echo "容器启动需要较长时间，请耐心等待 ..."
echo "访问: http://localhost:8080"