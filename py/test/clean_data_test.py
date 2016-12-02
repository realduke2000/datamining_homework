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

    def test_team_salary(self):
        f = open('../../resources/nba_info_utf8.txt')
        info_map = {}
        f.readline()
        # 12 - salary, 8 - team
        for line in f:
            data = line.split('|')
            if not data[12]:
                continue
            data[12] = data[12].strip().strip("万美元")
            if not data[8]:
                continue
            if data[8] in info_map:
                info_map[data[8]] = (info_map[data[8]][0] + 1, info_map[data[8]][1] + int(data[12])) # sum
            else:
                info_map[data[8]] = (1, int(data[12]))
        for k in info_map:
            print(k)
            print(str(info_map[k][1]/info_map[k][0])) # ave
            print

    def test_group_positio(self):
        f = open('../../resources/nba_info_utf8.txt')
        f.readline()
        position_info = {}
        for line in f:
            data = line.split("|")
            pos = data[5][:data[5].index('(')]
            if pos in position_info:
                position_info[pos] += 1
            else:
                position_info[pos] = 0
        for k in position_info:
            print("%s:%s"%(str(k),str(position_info[k])))

if __name__ == '__main__':
    unittest.main()
