# u2_save_torrents
一个u2自动放魔/拉孤种的脚本，调用了Azusa巨佬的api：https://github.com/kysdm/u2_api
运行逻辑：
每隔n小时连接qb，调用A佬api、获取孤种列表（并进行做种人数、类型筛选），检测Free状态并释放魔法，以上各项均可自定义

依赖：
pip install retry
pip install requests
pip install qbittorrent-api

使用方法：
填写config.py，直接运行main.py
其中token为A佬api所需，详见https://github.com/kysdm/u2_api
自动化鉴权脚本 https://greasyfork.org/zh-CN/scripts/428545

docker部署（仅限x86架构）：
下载config.py并填写内容
拉取镜像：
docker pull mkxiaolang/auto_save_torrents:latest
docker run \
  --name auto_save_torrents \
  -v /xxx/xxx/config.py:/auto_save_torrents/config.py \
 mkxiaolang/auto_save_torrents:latest
