#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2023/1/4 2:30
# @Author  : Small tred
# @FileName: biliBVencode.py
# @Software: PyCharm
# @Blog    : https://www.hecady.com
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


if __name__ == '__main__':
    print(BiliBv.bv2av('BV1S24y1w7rU'))
    print(BiliBv.av2bv('782405540'))
