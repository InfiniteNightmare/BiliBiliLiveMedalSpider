#!/usr/bin/env python3
# # -*- coding: utf-8 -*-
import requests
import json
import re
import time


def getHTML(url, params=None):
    try:
        headers = {'user-agent': 'Chrome/83'}
        r = requests.get(url, params=params, headers=headers)
        r.encoding = 'utf-8'
        r.raise_for_status
        return r.text
    except:
        return ''


def getRuid(roomid):
    try:
        url = 'https://live.bilibili.com/' + str(roomid)
        html = getHTML(url)
        uid = regex_ruid.search(html).group()
        return uid
    except:
        return AssertionError


def getMedal(roomid, ruid):
    try:
        url = 'https://api.live.bilibili.com/rankdb/v1/RoomRank/webMedalRank'
        params = {'roomid': roomid, 'ruid': ruid}
        medalinfo = getHTML(url, params=params)
        match = regex_medal.findall(medalinfo)
        if len(match) > 1:
            return match[1]
        else:
            return ''
    except:
        print('房间' + str(roomid) + '爬取失败', file=logfile)

medaldict = {}
regex_ruid = re.compile(r'(?<="uid":)\d*')
regex_medal = re.compile(r'(?<="medal_name":")[^"]*')
with open('settings.json', 'r') as f:
    settings = json.load(f)
    num1 = settings['num1']
    num2 = settings['num2']
num = num2 - num1 + 1
num_percent = max(num // 10000, 1)
with open('log.txt', 'w', encoding = 'utf-8') as logfile:
    print('爬取开始', file=logfile)
with open('medal.txt', 'w', encoding='utf-8') as medalfile:
    print('勋章字典：', file=medalfile)
for i in range(num1, num2):
    medalname = getMedal(i, getRuid(i))
    if medalname:
        with open('medal.txt', 'a', encoding='utf-8') as medalfile:
            print('{}:{}'.format(medalname, i), file=medalfile)
    if i % num_percent == 0:
        with open('log.txt', 'w', encoding = 'utf-8') as logfile:
            print('{} {}/{} {:.2f}% compelete'.format(time.ctime(),i - num1 + 1 , num, i * 100 / num), file=logfile)
with open('log.txt', 'a', encoding = 'utf-8') as logfile:
    print('爬取结束', file=logfile)
