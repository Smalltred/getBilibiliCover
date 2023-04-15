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

bv_url_file = open("bv_url.text", 'r', encoding='utf-8').readlines()
bv_id_file = open("bv_id.text", 'r', encoding='utf-8').readlines()
ep_url_file = open("ep_url.text", "r", encoding='utf-8').readlines()


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
def test_get_api():
    for i in ep_url_file:
        test = BilibiliCover(i)
        print(test.getVideoId())
        print('--------------------------')


if __name__ == '__main__':
    test_get_api()
    pass