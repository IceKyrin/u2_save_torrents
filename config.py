# qb连接设置
CLIENT_IP = '192.168.2.177'
CLIENT_PORT = 8080
CLIENT_USER = 'admin'
CLIENT_PASSWORD = 'adminadmin'

# 添加种子时，是否默认暂停（不自动开始下载）
paused = True
# 保存路径(如果是docker，则为容器内相对路径)
save_path = "/downloads/save_torrents"

# kysdm巨佬的api
# uid
uid = ""
# 自动化鉴权脚本，自动获取passkey https://greasyfork.org/zh-CN/scripts/428545
token = ""
# u2的cookie,从iyuu复制就行，下载种子用
cookie = ""

# 运行间隔（每n小时下载一次孤种）
interval = 24
# 设为False后，就变成只给大家放魔、自己不下载刷流的福利脚本
down = True
# 每次下载数量
download_num = 2

# 孤种筛选条件（最大/最小做种人数）
minimum = 1
maximum = 2

# 是否释放魔法，魔法持续时间，生效范围"ALL"/"SELF"
magic = True
magic_hours = 24
magic_scope = "ALL"

# 是否只保BDMV/DVDISO
BDMV = True
# 针对幼儿园需要代理访问的情况
proxy = True
proxies = {'http': "127.0.0.1:10801",
           'https': "127.0.0.1:10801"}
