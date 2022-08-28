# 所有选项除了注明外，填写True/False
# 存在老种永久Free不识别的情况，此种跳过。需要时间更新数据库
# qb连接设置
CLIENT_IP = '192.168.2.177'
CLIENT_PORT = 8080
CLIENT_USER = 'admin'
CLIENT_PASSWORD = 'adminadmin'

# 添加种子时，是否默认暂停（不自动开始下载）
paused = True
# 保存路径(如果是docker，则为容器内相对路径),add_id打开之后，路径会变成/save_path/种子id/种子名，套了一层名为id的文件夹（不明白默认False就可）
add_id = False
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
# 每次下载数量；只保BDMV/DVDISO时，一次3-5个就不少了，别太高
download_num = 2

# 孤种筛选条件（最大/最小做种人数）
minimum = 1
maximum = 2

# 非Free种、自己不放魔法头铁硬上（会产生下载量！！！）
tou_tie = False
# 是否释放魔法，每次最大花费（每金为10000），费用超了这个种子直接跳过不下。魔法持续时间最低24，生效范围"ALL"/"SELF"
magic = True
max_cost = 15000
magic_hours = 24
magic_scope = "ALL"
# 上传率1.3~2.33，下载0~0.8，不设范围检测，乱填炸了不负责
upload_ratio = 1.3
download_ratio = 0.00

# 蹭魔法有效期（蹭大佬的全局魔法，剩余n小时以上就蹭，否则自己释放，防止时间不够下载）
free_hours = 12
# 是否只保BDMV/DVDISO
BDMV = True
# 针对幼儿园需要代理访问的情况
proxy = True
proxies = {'http': "127.0.0.1:10801",
           'https': "127.0.0.1:10801"}
# SSL 我这网太差了才关的，能用就尽量True
verify = True
# 日志等级，默认INFO,嫌吵改成WARN（大写）
level = "INFO"
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ApplewebKit/537.36 (KHtml, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
}
