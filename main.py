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
from loguru import logger

# 日志文件
LOG_DIR = os.path.expanduser("./logs")
LOG_FILE = os.path.join(LOG_DIR, "file_{time}.log")
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)
logger.add(LOG_FILE, rotation="7 days", level=config.level, backtrace=True, diagnose=True, encoding="utf-8")

header = config.header


def download_torrent(torrent_id):
    url = "https://u2.dmhy.org/download.php?id=%s" % torrent_id
    try:
        if config.proxy:
            r = requests.get(url, headers=header, proxies=config.proxies, timeout=30, verify=config.verify)  # 发送请求
        else:
            r = requests.get(url, headers=header, timeout=20, verify=config.verify)  # 发送请求
        # 保存
        with open('./torrents/%s.torrent' % torrent_id, 'wb') as f:
            f.write(r.content)
        logger.debug("种子下载完毕")

    except Exception as e:
        logger.warning(e)
        logger.warning("种子下载失败")


@retry(tries=3, delay=2)
def magic_use(sta, torrent_id):
    use = "" if sta else "test=1"
    url = "https://u2.dmhy.org/promotion.php?" + use
    data = {"action": "magic",
            "base_everyone": 1200,
            "base_other": 500,
            "base_self": 350,
            "comment": None,
            "divergence": 9.331,
            "dr": config.download_ratio,
            "hours": config.magic_hours,
            "promotion": 2,
            "start": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "torrent": torrent_id,
            "tsize": round(time.time()),
            "ur": config.upload_ratio,
            "user": config.magic_scope,
            "user_other": None}
    try:
        if config.proxy:
            res = requests.post(url=url, data=data, headers=header, proxies=config.proxies, timeout=8,
                                verify=config.verify)
        else:
            res = requests.post(url=url, data=data, headers=header, verify=config.verify)
        if str(res) == '<Response [200]>' and sta:
            logger.info("魔法释放成功")
            return True
        elif str(res) == '<Response [200]>' and not sta:
            cost = int(re.search("title=.*?([\d,]*\.\d{,2}).*?>", res.text).group(1).split(".")[0].replace(",", ""))
            logger.debug("获取魔法费用成功")
            return cost
        return False
    except Exception as e:
        logger.warning(e)


def compare_time(t1, t2):
    try:
        t0 = int(str(round(time.time())))
        t1 = int(time.mktime(time.strptime(t1, '%Y-%m-%dT%H:%M:%S')))
        t2 = int(time.mktime(time.strptime(t2, '%Y-%m-%dT%H:%M:%S')))
        if t0 > t1:
            return t2 - t1
        else:
            return 0
    except Exception as e:
        logger.warning(e)


@retry(tries=5, delay=2)
def magic_sta(torrent_id):
    url = "https://u2.kysdm.com/api/v1/promotion_super/?token=%s&uid=%s&torrent_id=%s" % (
        config.token, config.uid, torrent_id)
    res = requests.get(url, timeout=8).text
    magic_ratio = json.loads(res)["data"]["promotion_super"][0]["ratio"]
    ratio = float(magic_ratio.split("/")[-1])
    return ratio


@retry(tries=5, delay=2)
def magic_free_time(torrent_id):
    url = "https://u2.kysdm.com/api/v1/promotion_specific/?token=%s&uid=%s&torrent_id=%s" % (
        config.token, config.uid, torrent_id)
    res = requests.get(url, timeout=8).text
    magic_list = json.loads(res)["data"]["promotion"]
    time_list = []
    for i in magic_list:
        ratio = float(i["ratio"].split("/")[-1])
        # 全局生效、下载为0的才计入Free
        if i["torrent_name"] == "全局" and ratio == 0:
            if i["expiration_time"] is None:
                t = 3600 * 24 * 365
            else:
                t = compare_time(i["from_time"], i["expiration_time"])
            time_list.append(t)
        else:
            time_list.append(0)
    logger.debug(time_list)
    return max(time_list)


@retry(tries=5, delay=2)
def get_torrent(num):
    url = "https://u2.kysdm.com/api/v1/torrent_low_seed/?token=%s&uid=%s&minseeder=%s&maxseeder=%s&maximum=%s" % (
        config.token, config.uid, config.minimum, config.maximum, config.download_num * num)
    res = requests.get(url, timeout=8).text
    torrent_list = json.loads(res)["data"]["torrent"]
    return torrent_list


def hash_to_id(torrent_hash):
    url = "https://u2.kysdm.com/api/v1/history/?token=%s&maximum=1&uid=%s&hash=%s" % (
        config.token, config.uid, torrent_hash)
    res = requests.get(url, timeout=8).text
    torrent_id = json.loads(res)["data"]["history"][0]["torrent_id"]
    return torrent_id


def push_torrent(torrent_id, file_name):
    path = config.save_path
    if config.add_id:
        path = path + "/%s/" % torrent_id
    qbt_client.torrents_add(torrent_files=file_name, save_path=path, is_paused=config.paused)


def pluck(lst, key):
    return [x.get(key) for x in lst]


def qb_login():
    try:
        # 登陆
        qbt_client = qbittorrentapi.Client(host=config.CLIENT_IP, port=config.CLIENT_PORT, username=config.CLIENT_USER,
                                           password=config.CLIENT_PASSWORD)
        qbt_client.auth_log_in()
        logger.info("登录qb成功")
        return qbt_client
    except Exception as e:
        logger.warning(e)
        logger.warning("登录失败，请检查qb webui 的ip、端口及账号密码")


header["cookie"] = config.cookie
if not os.path.exists("torrents"):
    os.mkdir("torrents")
while True:
    qbt_client = qb_login()
    try:
        if config.BDMV:
            # 获取下载数x50的列表
            raw_lists = get_torrent(50)
            logger.debug("拉取孤种列表成功")
            torrent_lists = []
            # 筛选出原盘
            for info in raw_lists:
                if info["category"] == "BDMV" or info["category"] == "DVDISO":
                    torrent_lists.append(info)
        else:
            # 获取下载数x5的列表
            torrent_lists = get_torrent(5)
            logger.debug("拉取孤种列表成功")
        # 随机筛选出下载的种子（防止拉孤种时和其他人撞车）
        res_id = pluck(torrent_lists, 'torrent_id')
        if len(res_id) >= config.download_num:
            download_list = random.sample(res_id, config.download_num)
        else:
            logger.info("原盘孤种较少，本次不推送，开始待机")
            time.sleep(config.interval * 3600)
            continue
        logger.debug(download_list)
        # 遍历种子
        for t_id in download_list:
            logger.info("当前种子id为：%s" % t_id)
            # Free剩余时间大于设定值
            if magic_free_time(t_id) > config.free_hours * 3600:
                magic_res = True
                logger.info("蹭到了其他大佬的Free")
            # elif magic_sta(t_id) == 0:
            #    logger.info("此种Free,无法判断剩余时间")
            #    magic_res = True
            else:  # 非Free种
                # 释放魔法
                if config.magic:
                    logger.debug("准备释放魔法")
                    m_cost = magic_use(False, t_id)
                    # 判断释放魔法并下载，或跳过（花费过高）
                    if m_cost < config.max_cost:
                        magic_res = magic_use(config.magic, t_id)
                    else:
                        logger.info("魔法花费过高:%s,跳过此种子" % m_cost)
                        continue
                # 头铁硬上
                else:
                    magic_res = False
            if config.down:  # 下载开关
                # Free存在或头铁硬上
                if magic_res or config.tou_tie:
                    for _ in range(3):
                        if os.path.exists("./torrents/%s.torrent" % t_id):
                            logger.debug("种子已存在")
                            push_torrent(t_id, "./torrents/%s.torrent" % t_id)
                            logger.info("种子推送完毕")
                            break
                        else:
                            logger.debug("id：%s 种子开始下载" % t_id)
                            download_torrent(t_id)
                else:
                    logger.info("非Free种且未释放魔法，跳过")
    except Exception as e:
        logger.warning(e)
    logger.info("本次流程完毕，开始待机")
    time.sleep(config.interval * 3600)
