#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
import re
import time


def getHTML(url, params=None):  # 爬取网页，获得网页HTML
    try:
        headers = {'user-agent': 'Chrome/83'}  # 伪造请求头
        r = requests.get(url, params=params, headers=headers)  # 提交请求，并获得响应
        r.encoding = 'utf-8'  # b站直播采用utf-8编码
        r.raise_for_status  # 如果状态码不为200即爬取失败则产生异常
        return r.text  # 返回网页HTML
    except:
        return ''  # 异常处理


def getRuid(roomid):    # 获取主播b站id
    try:
        url = 'https://live.bilibili.com/' + str(roomid)  # 直播间url
        html = getHTML(url)  # 获得直播间HTML
        uid = regex_ruid.search(html).group()  # 通过正则表达式匹配直播间HTML，获取主播id
        return uid  # 返回主播id
    except:
        return AssertionError  # 异常处理


def getMedal(roomid, ruid):  # 获取粉丝勋章
    try:
        url = 'https://api.live.bilibili.com/rankdb/v1/RoomRank/webMedalRank'  # 查询粉丝勋章的网页api
        params = {'roomid': roomid, 'ruid': ruid}  # 需要房间号和主播b站id作为参数
        medalinfo = getHTML(url, params=params)  # 返回查询结果
        match = regex_medal.findall(medalinfo)  # 通过正则表达式匹配查询结果，获取粉丝勋章名称
        if len(match) > 1:  # 如果该直播间开通了粉丝勋章且粉丝榜有粉丝
            return match[1]  # 返回获取粉丝勋章名称
        else:
            return ''  # 否则返回空字符串
    except:  # 异常处理
        with open('medal.txt', 'a', encoding='utf-8') as medalfile:
            # 在"medal.txt"中添加错误记录
            print('房间' + str(roomid) + '爬取失败', file=medalfile)


# 程序入口
regex_ruid = re.compile(r'(?<="uid":)\d*')  # 用于匹配主播id的正则表达式
regex_medal = re.compile(r'(?<="medal_name":")[^"]*')  # 用于匹配粉丝勋章的正则表达式
with open('settings.json', 'r') as f:  # 读取配置文件
    settings = json.load(f)
    num1 = settings['num1']
    num2 = settings['num2']
# 初始化相关参数
num = num2 - num1 + 1  # 爬取的房间总数
num_percent = max(num // 10000, 1)  # 用于显示进度的基数
with open('log.txt', 'w', encoding='utf-8') as logfile:  # 清空"log.txt"
    print('爬取开始', file=logfile)
with open('medal.txt', 'w', encoding='utf-8') as medalfile:  # 清空"medal.txt"
    print('勋章字典：', file=medalfile)
for i in range(num1, num2):  # 遍历直播间
    # 先调用getRuid()函数获取该直播间主播id，再用房间号和主播id为参数调用getMedal()获取粉丝勋章
    medalname = getMedal(i, getRuid(i))
    if medalname:  # 如果该直播间开通了粉丝勋章且粉丝榜有粉丝
        with open('medal.txt', 'a', encoding='utf-8') as medalfile:  # 以追加模式打开"medal.txt"，注意编码格式
            print('{}:{}'.format(medalname, i),
                  file=medalfile)  # 写入粉丝勋章及其对应的房间号
    if i % num_percent == 0:  # 显示进度
        with open('log.txt', 'w', encoding='utf-8') as logfile:  # 以写入模式打开"log.txt"
            print('{} {}/{} {:.2f}% compelete'.format(time.ctime(),
                                                      i - num1 + 1, num, (i - num1) * 100 / num), file=logfile)  # 输出当前时间、进度，增强用户体验
with open('log.txt', 'a', encoding='utf-8') as logfile:
    print('爬取结束', file=logfile)  # 爬取完毕，输出提示信息
