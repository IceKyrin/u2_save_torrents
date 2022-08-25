# coding=utf-8
# ! /usr/bin/python
import re
import os
import time
import json
import config
import random
import requests
import datetime
import qbittorrentapi
from retry import retry

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ApplewebKit/537.36 (KHtml, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
}


def download_torrent(torrent_id):
    url = "https://u2.dmhy.org/download.php?id=%s" % torrent_id
    try:
        if config.proxy:
            r = requests.get(url, headers=header, proxies=config.proxies, timeout=30, verify=False)  # 发送请求
        else:
            r = requests.get(url, headers=header, timeout=20, verify=False)  # 发送请求
    except Exception as e:
        print(e)
        try:
            if config.proxy:
                r = requests.get(url, headers=header, proxies=config.proxies, timeout=30, verify=False)  # 发送请求
            else:
                r = requests.get(url, headers=header, timeout=20, verify=False)  # 发送请求
        except Exception as e:
            print(e)
    # 保存
    with open('./torrents/%s.torrent' % torrent_id, 'wb') as f:
        f.write(r.content)
    print("种子下载完毕")


@retry(tries=2, delay=15)
def magic_use(sta, torrent_id):
    use = "" if sta else "test=1"
    url = "https://u2.dmhy.org/promotion.php?" + use
    data = {"action": "magic",
            "base_everyone": 1200,
            "base_other": 500,
            "base_self": 350,
            "comment": None,
            "divergence": 9.331,
            "dr": 1.00,
            "hours": config.magic_hours,
            "promotion": 2,
            "start": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "torrent": torrent_id,
            "tsize": round(time.time()),
            "ttl": 526,
            "ur": 1.00,
            "user": config.magic_scope,
            "user_other": None}
    if magic_sta(torrent_id) != 0:
        if config.proxy:
            res = requests.post(url=url, data=data, headers=header, proxies=config.proxies, timeout=5,
                                verify=False).text
        else:
            res = requests.post(url=url, data=data, headers=header, verify=False).text
        # cost = int(re.search("title=.*?([\d,]*\.\d{,2}).*?>", res).group(1).split(".")[0].replace(",", ""))
    return res


@retry(tries=5, delay=1)
def magic_sta(torrent_id):
    url = "https://u2.kysdm.com/api/v1/promotion_super/?token=%s&uid=%s&torrent_id=%s" % (
        config.token, config.uid, torrent_id)
    res = requests.get(url, timeout=3).text
    state = json.loads(res)["data"]["promotion_super"][0]["ratio"]
    ratio = float(state.split("/")[-1])
    return ratio


@retry(tries=5, delay=2)
def get_torrent(num):
    url = "https://u2.kysdm.com/api/v1/torrent_low_seed/?token=%s&uid=%s&minseeder=%s&maxseeder=%s&maximum=%s" % (
        config.token, config.uid, config.minimum, config.maximum, config.download_num * num)
    res = requests.get(url, timeout=8).text
    torrent_list = json.loads(res)["data"]["torrent"]
    return torrent_list


def push_torrent(file_name):
    qbt_client.torrents_add(torrent_files=file_name, save_path=config.save_path, is_paused=config.paused)


def pluck(lst, key):
    return [x.get(key) for x in lst]


header["cookie"] = config.cookie
if not os.path.exists("torrents"):
    os.mkdir("torrents")
while True:
    try:
        # 登陆
        qbt_client = qbittorrentapi.Client(host=config.CLIENT_IP, port=config.CLIENT_PORT, username=config.CLIENT_USER,
                                           password=config.CLIENT_PASSWORD)
        qbt_client.auth_log_in()
        print("登录qb成功")
    except Exception as e:
        print(e)
        print("登录失败，请检查qb webui 的ip、端口及账号密码")
    try:
        if config.BDMV:
            # 获取下载数x20的列表
            raw_lists = get_torrent(20)
            print("拉取孤种列表成功")
            torrent_lists = []
            # 筛选出原盘
            for info in raw_lists:
                if info["category"] == "BDMV" or info["category"] == "DVDISO":
                    torrent_lists.append(info)
        else:
            # 获取下载数x5的列表
            torrent_lists = get_torrent(5)
            print("拉取孤种列表成功")
        # 随机筛选出下载的种子（防止拉孤种时和其他人撞车）
        download_list = random.sample(pluck(torrent_lists, 'torrent_id'), config.download_num)
        print(download_list)
        for t_id in download_list:
            print(t_id)
            if magic_sta(t_id) == 0:
                print("蹭到了其他大佬的Free")
            else:
                if config.magic:
                    print("准备释放魔法")
                    magic_use(config.magic, t_id)
                    print("魔法释放完毕")
            if config.down:
                for _ in range(3):
                    if os.path.exists("./torrents/%s.torrent" % t_id):
                        print("种子已存在")
                        push_torrent("./torrents/%s.torrent" % t_id)
                        print("种子推送完毕")
                        break
                    else:
                        print("id：%s 种子开始下载" % t_id)
                        download_torrent(t_id)
    except Exception as e:
        print(e)
    print("开始待机")
    time.sleep(config.interval * 3600)
