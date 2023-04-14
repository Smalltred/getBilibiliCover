#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2023/4/14 6:49
# @Author  : Small tred
# @FileName: bilibiliCover.py
# @Software: PyCharm
# @Blog    : https://www.hecady.com
import requests
import re

table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
tr = {}
for i in range(58):
    tr[table[i]] = i
s = [11, 10, 3, 8, 4, 6]
xor = 177451812
add = 8728348608


class BiliBv:

    # BV转AV
    @staticmethod
    def bv2av(x):
        if len(x) == 11:
            x = "BV1" + x[2:]
        r = 0
        for i in range(6):
            r += tr[x[s[i]]] * 58 ** i
        return (r - add) ^ xor

    # AV转BV
    @staticmethod
    def av2bv(x):
        y = int(x)
        y = (y ^ xor) + add
        r = list('BV1  4 1 7  ')
        for i in range(6):
            r[s[i]] = table[y // 58 ** i % 58]
        return ''.join(r)


class BilibiliCover(BiliBv):
    url = "https://www.bilibili.com/"
    av = "av"
    api = {
        "bv": "https://api.bilibili.com/x/web-interface/view?bvid=",
        "av": "https://api.bilibili.com/x/web-interface/view?bvid=",
        "ep": "https://api.bilibili.com/pgc/view/web/season?ep_id=",
        "ss": "https://api.bilibili.com/pgc/view/web/season?season_id=",
        "md": "https://api.bilibili.com/pgc/web/season/section?season_id="
    }

    id_type = None

    def __init__(self, string):
        self.string = string

    def regex_url(self):
        """
        1.判断是否为链接
        2.判断是否为b23.tv
        3.判断是否为bilibili.com
        4.判断是否为b23.tv重定向后的真实地址
        :return: https://www.bilibili.com/video/BV1S24y1w7rU/ or self.string
        """
        result = None
        url = re.search(r"[a-zA-z]+://[^\s]*", self.string)
        if url:
            b23_pattern = r'https?://b23\.tv/[\w-]+'
            bilibili_pattern = r'https?://www\.bilibili\.com/video/[\w-]+'
            if re.match(b23_pattern, url.group(0)):
                result = self.redirect_url(url.group(0))
            if re.match(bilibili_pattern, url.group(0)):
                result = url.group(0)
        else:
            result = self.string
        return result

    @staticmethod
    def redirect_url(url):
        """
        对b23.tv进行重定向，获取真实地址
        :param url: 【xxx-哔哩哔哩】 https://b23.tv/hMwMJ70
        :return:
        """
        r = requests.get(url, allow_redirects=False)
        if r.status_code == 301 or r.status_code == 302:
            location = r.headers['Location']
            return location
        return None

    def get_video_id(self):
        """
        正则匹配 内容是否包含视频ID
        :return: BV1S24y1w7rU、av号匹配成功转为bv号、ep743051、ss26266、md28229233
        :return {"code": -404, "message": "请检查内容是否包含视频ID"}
        ep号 ss号 md号 不带前缀
        """
        id_dict = {
            "bv": self.regexBv,
            "av": self.regexAv,
            "ep": self.regexEp,
            "ss": self.regexSs,
            "md": self.regexMd
        }
        url_regex_result = self.regex_url()
        for id_type, regex_func in id_dict.items():
            id_regex_result = regex_func(url_regex_result)
            if id_regex_result:
                self.id_type = id_type
                return id_regex_result
        return {"code": -404, "message": "请检查内容是否包含视频ID"}

    def regexAv(self, string):
        """匹配av号"""
        """自动转为bv号"""
        regex = re.compile(r"(av.*?)\d+", re.I)
        av_id = regex.search(string)
        if av_id:
            return self.av2bv(av_id.group(0)[2:])

    @staticmethod
    def regexBv(string):
        """匹配BV号"""
        regex = re.compile(r'(BV.*?).{10}', re.I)
        bv_id = regex.search(string)
        if bv_id:
            return bv_id.group(0)

    @staticmethod
    def regexEp(string):
        """匹配EP号"""
        regex = re.compile(r"(ep.*?)\d+", re.I)
        ep_id = regex.search(string)
        if ep_id:
            return ep_id.group(0)[2:]

    @staticmethod
    def regexSs(string):
        """匹配SS号"""
        regex = re.compile(r"(ss.*?)\d+", re.I)
        ss_id = regex.search(string)
        if ss_id:
            return ss_id.group(0)[2:]

    @staticmethod
    def regexMd(string):
        """匹配Med号"""
        regex = re.compile(r"(md.*?)\d+")
        md_id = regex.search(string)
        if md_id:
            return md_id.group(0)[2:]

    def requestMiddleware(self):
        """
        请求中间件 对传入的video_id进行检查
        :return: 成功返回 对应请求json对象 失败 返回响应错误代码
        :return {"code": -404, "message": "请检查内容是否包含视频ID"}
        :return {'code': -400, 'message': '获取封面失败'}
        """
        video_id = self.get_video_id()
        if not isinstance(video_id, dict):
            api = self.api.get(self.id_type)
            response = requests.get(api + video_id)
            error_codes = {-400, -404}
            if response.json()['code'] == 0:
                return response
            if response.json()['code'] in error_codes:
                return {'code': -400, 'message': '获取封面失败'}
        return video_id
