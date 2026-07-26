#
# CentOS7安装，需要root权限
# https://docs.docker.com/engine/install/centos/
#

# 安装依赖
yum install -y yum-utils

# 添加 Docker 官方仓库
# yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
# 替换国内yum源
yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

# 安装最新版本的 Docker CE
yum install -y docker-ce docker-ce-cli containerd.io

# 启动并设置开机启动
systemctl enable --now docker

# 添加docker用户组
groupadd docker
usermod -aG docker other_user
newgrp docker

# 重启docker
systemctl daemon-reload
systemctl restart docker

# 验证安装是否成功
docker run hello-world