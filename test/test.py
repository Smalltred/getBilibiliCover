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
ss_file = open("ss.text", "r", encoding="utf-8").readlines()


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print("Time:", time.time() - start)
        return result

    return wrapper


@timer
def test_get_str(string):
    test = BilibiliCover(string)
    print(test.cover())
    print('--------------------------')


@timer
def test_get_url():
    test = BilibiliCover("https://www.bilibili.com/video/BV1Z54y1b7mE")
    print(test.cover())
    print('--------------------------')


@timer
def test_all():
    # for i in bv_file:
    #     test = BilibiliCover(i)
    #     print(test.cover())
    #     print(test.video_id)
    #     print('--------------------------')
    # for i in av_file:
    #     test = BilibiliCover(i)
    #     print(test.cover())
    #     print(test.video_id)
    #     print('--------------------------')
    # for i in ep_file:
    #     test = BilibiliCover(i)
    #     print(test.cover())
    #     print(test.video_id)
    #     print('--------------------------')
    # for i in ss_file:
    #     test = BilibiliCover(i)
    #     print(test.cover())
    #     print('--------------------------')
    for i in md_file:
        test = BilibiliCover(i)
        print(test.cover())
        print(test.video_id)
        print('--------------------------')


if __name__ == '__main__':
    # test_get_str(
        # "https://i2.hdslb.com/bfs/archive/79b6933cbc49ffe3c853e4ce42eb1e25f6223311.jpg@672w_378h_1c_!web-home-common-cover.avif")
    test_all()
