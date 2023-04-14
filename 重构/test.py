#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2023/4/14 7:01
# @Author  : Small tred
# @FileName: test.py
# @Software: PyCharm
# @Blog    : https://www.hecady.com
from bilibiliCover import BilibiliCover
import time

test_url_ls = [
    '【《三体》 第15话 永恒的篝火-哔哩哔哩国创】https://b23.tv/ep705756',
    'https://www.bilibili.com/video/BV1S24y1w7rU/',
    'https://b23.tv/ep705756',
    'https://b23.tv/ep705756',
    'https://b23.tv/ep705756',
    'https://b23.tv/hMwMJ70',
    'https://www.bilibili.com/video/av1564'
]

test_str_ls = [
    'ss40156',
    'ep705756',
    'hMwMJ70',
    'av1564asd',
    'ss40156ads',
    'ep705756sad',
    'hMwMJ70asd',
    'av1564asdasd',
    'BV1advsqsxad'

]


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print("Time:", time.time() - start)
        return result

    return wrapper


def test_url():
    for i in test_url_ls:
        test = BilibiliCover(i)
        print(test.get_bili_url())


@timer
def test_get_url_id():
    for i in test_url_ls:
        test = BilibiliCover(i)
        print(test.get_video_id())


@timer
def test_get_str_id():
    for i in test_str_ls:
        test = BilibiliCover(i)
        print(test.get_video_id())


if __name__ == '__main__':
    test_get_url_id()
    print('--------------------------')
    test_get_str_id()
