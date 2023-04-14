#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2023/4/14 6:49
# @Author  : Small tred
# @FileName: bilibiliCover.py
# @Software: PyCharm
# @Blog    : https://www.hecady.com
import requests
import re
from biliBVencode import BiliBv


class BilibiliCover(BiliBv):
    url = "https://www.bilibili.com/"
    av = "av"
    bv_api = "https://api.bilibili.com/x/web-interface/view?bvid="
    ep_api = "https://api.bilibili.com/pgc/view/web/season?ep_id="
    ss_api = "https://api.bilibili.com/pgc/view/web/season?season_id="
    md_api = "https://api.bilibili.com/pgc/review/user?media_id="
    md_all_api = "https://api.bilibili.com/pgc/web/season/section?season_id="
    id_type = None
    error = None

    def __init__(self, string):
        self.string = string

    def get_bili_url(self):
        """
        1.判断是否为链接
        2.判断是否为b23.tv
        3.判断是否为bilibili.com
        4.判断是否为b23.tv重定向后的真实地址
        :return: https://www.bilibili.com/video/BV1S24y1w7rU/
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
        return result

    def get_video_id(self):
        """
        :return:
        """
        url = self.get_bili_url()
        if url:
            return self.regexId(url)
        else:
            return self.regexId(self.string)

    @staticmethod
    def redirect_url(url):
        r = requests.get(url, allow_redirects=False)
        if r.status_code == 301 or r.status_code == 302:
            location = r.headers['Location']
            return location
        return None

    def regexId(self, string):
        id_dict = {
            "bv": self.regexBv,
            "av": self.regexAv,
            "ep": self.regexEp,
            "ss": self.regexSs,
            "md": self.regexMd
        }
        for id_type, regex_func in id_dict.items():
            result = regex_func(string)
            if not isinstance(result, tuple):
                self.id_type = id_type
                return result
            else:
                self.error = result[1]
                self.id_type = None

    def regexAv(self, string):
        """匹配av号"""
        """自动转为bv号"""
        regex = re.compile(r"(av.*?)\d+", re.I)
        av_id = regex.search(string)
        if av_id:
            return self.av2bv(av_id.group(0)[2:])
        return None, "No AV found"

    @staticmethod
    def regexBv(string):
        """匹配BV号"""
        regex = re.compile(r'(BV.*?).{10}', re.I)
        bv_id = regex.search(string)
        if bv_id:
            return bv_id.group(0)
        return None, "No BV found"

    @staticmethod
    def regexEp(string):
        """匹配EP号"""
        regex = re.compile(r"(ep.*?)\d+", re.I)
        ep_id = regex.search(string)
        if ep_id:
            return ep_id.group(0)[2:]
        return None, "No EP found"

    @staticmethod
    def regexSs(string):
        """匹配SS号"""
        regex = re.compile(r"(ss.*?)\d+", re.I)
        ss_id = regex.search(string)
        if ss_id:
            return ss_id.group(0)[2:]
        return None, "No SS found"

    @staticmethod
    def regexMd(string):
        """匹配Med号"""
        regex = re.compile(r"(md.*?)\d+")
        md_id = regex.search(string)
        if md_id:
            return md_id.group(0)[2:]
        return None, "No MD found"

    def requestMiddleware(self, id_type, api, params):
        pass
