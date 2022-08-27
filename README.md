# u2_save_torrents

一个u2自动放魔/拉孤种的脚本，调用了Azusa巨佬的api：https://github.com/kysdm/u2_api


运行逻辑：

每隔n小时连接qb，调用A佬api、获取孤种列表（并进行做种人数、类型筛选），检测Free状态并释放魔法，以上各项均可自定义

！！！！！！！！

这个版本是映射整个文件夹，不单单是config.py

一定要给脚本所在文件夹授予读写权限（尤其是群晖docker），否则可能无法产生log、下载种子

！！！！！！！！

依赖（docker方式不装）：

pip install retry

pip install loguru

pip install requests

pip install qbittorrent-api


使用方法：

填写config.py，python main.py 或 python3 main.py（看你自己装的环境）

其中token为A佬api所需，详见https://github.com/kysdm/u2_api

自动化鉴权脚本 https://greasyfork.org/zh-CN/scripts/428545

脚本会自动生成log文件夹，torrents文件夹（保存下载的种子，可以硬链接到qb、tr监控文件夹内）


docker部署（仅限x86架构）：

下载main.py和config.py到文件夹xyz，并填写config.py内容

拉取镜像：

docker pull mkxiaolang/auto_save_torrents:latest

使用命令行

docker run \
  --name auto_save_torrents \
  -v /xxx/xyz:/auto_save_torrents \
 mkxiaolang/auto_save_torrents:latest

或gui界面，将xyz文件夹映射到/auto_save_torrents
