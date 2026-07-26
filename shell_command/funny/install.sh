#!/bin/bash
#
# install funny commands
#

FUNNY_COMMANDS="fortune cowsay cmatrix"

# for raspberrypi
uname -a | grep Debian
if [ $? -eq 0 ]; then
    for command in `echo ${FUNNY_COMMANDS}`; do
        echo "INSTALLING ${command} ..."
        echo "----------"
        sudo apt install ${command}
    done
fi

# for Mac
uname -a | grep Darwin
if [ $? -eq 0 ]; then
    for command in `echo ${FUNNY_COMMANDS}`; do
        echo "INSTALLING ${command} ..."
        echo "----------"
        brew install ${command}
    done
fi

# 生成dat文件
#
# unzip fortune-zh.zip
# cd fortune-zh
# strfile tang300 tang300.dat
#
# 查看fortune目录
# fortune -f
