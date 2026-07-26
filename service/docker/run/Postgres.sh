mkdir -p ${HOME}/Docker/Postgres/data

docker rm -f Postgres
docker run -d \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=openstreetmap \
  -e POSTGRES_DB=postgres \
  -p 5432:5432 \
  -v ${HOME}/Docker/Postgres/data:/var/lib/postgresql/data \
  -e TZ=Asia/Shanghai \
  --restart unless-stopped \
  --name Postgres \
  postgres

echo "测试连接 ..."
echo "psql postgresql://postgres:openstreetmap@localhost:5432/postgres"
sleep 3
psql postgresql://postgres:openstreetmap@localhost:5432/postgres