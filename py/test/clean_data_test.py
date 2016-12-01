#!/usr/bin/python
#coding:utf-8

import os
import unittest
from unittest import TestCase

import sys


class Test(TestCase):
    def test_print_info_index(self):
        s = u'ID|name|个人网址|个人头像|身高|位置|体重|生日|球队|学校|选秀|出生地|本赛季薪金|合同|常规赛参加情况|季后赛参加情况'.split(u'|')
        for i in range(len(s)):
            sys.stdout.write(str(i) + ": " + s[i] + '\t')
            if i and i % 5 == 0:
                sys.stdout.write(os.linesep)

    def test_print_race_after_index(self):
        s = u'ID|name|赛季|球队|场次|首发|时间|投篮命中|投篮出手|命中率|三分命中|三分得手|命中率|罚球命中|罚球出手|命中率|篮板|助攻|抢断|盖帽|失误|犯规|得分'.split(u'|')
        for i in range(len(s)):
            sys.stdout.write(str(i) + ": " + s[i] + '\t')
            if i and i % 5 == 0:
                sys.stdout.write(os.linesep)

    def test_print_race_before_index(self):
        s = u'ID|name|赛季|球队|场次|首发|时间|投篮|命中率|三分|命中率|罚球|命中率|篮板|助攻|抢断|盖帽|失误|犯规|得分'.split(u'|')
        for i in range(len(s)):
            sys.stdout.write(str(i) + ": " + s[i] + '\t')
            if i and i % 5 == 0:
                sys.stdout.write(os.linesep)

if __name__ == '__main__':
    unittest.main()
