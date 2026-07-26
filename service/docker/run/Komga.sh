# https://komga.shrg/docs/installation/docker

mkdir -p ${HOME}/Docker/Komga/config
mkdir -p ${HOME}/Image  

docker rm -f Komga
docker run -d \
  --user 1000:1000 \
  -p 25600:25600 \
  --mount type=bind,source=${HOME}/Docker/Komga/config,target=/config \
  --mount type=bind,source=${HOME}/Image,target=/data \
  -e TZ=Asia/Shanghai \
  --restart unless-stopped \
  --name=Komga \
  gotson/komga

echo "访问: http://localhost:25600"