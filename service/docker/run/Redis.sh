mkdir -p ${HOME}/Docker/Redis/data

docker rm -f Redis
docker run -d \
  -p 6379:6379 \
  -v ${HOME}/Docker/Redis/data:/data \
  -e TZ=Asia/Shanghai \
  --restart unless-stopped \
  --name Redis \
  redis

echo "测试连接 ..."
echo "redis-cli -host localhost -p 6379"
sleep 3
redis-cli -h localhost -p 6379 ping