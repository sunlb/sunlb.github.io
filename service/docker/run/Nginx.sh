mkdir -p ${HOME}/Docker/Nginx/conf
mkdir -p ${HOME}/Docker/Nginx/html

docker rm -f Nginx
docker run -d \
  -p 80:80 \
  -v ${HOME}/Docker/Nginx/conf:/etc/nginx/conf.d \
  -v ${HOME}/Docker/Nginx/html:/usr/share/nginx/html \
  -e TZ=Asia/Shanghai \
  --restart unless-stopped \
  --name Nginx \
  nginx

echo "访问: http://localhost"