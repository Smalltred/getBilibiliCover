#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2023/4/14 7:01
# @Author  : Small tred
# @FileName: test.py
# @Software: PyCharm
# @Blog    : https://www.hecady.com
import re
from bilibiliCover import BilibiliCover
import time

bv_file = open("bv.text", "r", encoding="utf-8").readlines()
av_file = open("av.text", "r", encoding="utf-8").readlines()
ep_file = open("ep.text", "r", encoding="utf-8").readlines()
md_file = open("md.text", "r", encoding="utf-8").readlines()


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print("Time:", time.time() - start)
        return result

    return wrapper


def regexEp(string):
    regex = re.compile(r"(ep.*?)\d+", re.I)
    ep_id = regex.search(string)
    if ep_id:
        return ep_id.group(0)[2:]


@timer
def test_get():
    for i in bv_file:
        test = BilibiliCover(i)
        print(test.cover())
        print('--------------------------')


@timer
def test_all():
    for i in bv_file:
        test = BilibiliCover(i)
        print(test.cover())
        print(test.video_id)
        print('--------------------------')
    for i in ep_file:
        test = BilibiliCover(i)
        print(test.cover())
        print(test.video_id)
        print('--------------------------')
    for i in md_file:
        test = BilibiliCover(i)
        print(test.cover())
        print(test.video_id)
        print('--------------------------')


if __name__ == '__main__':
    test_get()
    # test_all()
    # 直接把分析结果打印到控制台
    pass
