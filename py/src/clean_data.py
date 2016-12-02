#!/usr/bin/python
#coding:utf-8
import argparse
import os

import sys
import time
import datetime


def print_gbk_str(file_path):
    with open(file_path) as f:
        for line in f:
            sys.stdout.write(line.decode('gb2312'))


def clean_chgui(race_file_path, new_file_path):
    """
    before:
    0: ID	1: name	2: 赛季	3: 球队	4: 场次	5: 首发
    6: 时间(1997-2013?)	7: 投篮	8: 命中率	9: 三分	10: 命中率
    11: 罚球	12: 命中率	13: 篮板	14: 助攻	15: 抢断
    16: 盖帽	17: 失误	18: 犯规	19: 得分
    after:
    0: ID	1: name	2: 赛季	3: 球队	4: 场次	5: 首发
    6: 时间	7: 投篮命中	8: 投篮出手	9: 命中率	10: 三分命中
    11: 三分得手	12: 命中率	13: 罚球命中	14: 罚球出手	15: 命中率
    16: 篮板	17: 助攻	18: 抢断	19: 盖帽	20: 失误
    21: 犯规	22: 得分
    :param race_file_path:
    :return:
    """
    title_race = 'ID|name|season|team|changci|shoufa|time|toulan_mingzhong|toulan_chusou|mingzhonglv|3fen_mingzhong|3fen_chushou|3fenmingzhonglv|faqiu_mingzhong|faqiu_chushou|faqiu_mingzhonglv|lanban|zhugong|qiangduan|gaimao|shiwu|fangui|defen'
    with open(new_file_path, mode='w') as new_chgui:
        with open(race_file_path, mode='r') as orig_chgui:
            new_chgui.write(title_race + os.linesep)
            orig_chgui.readline()
            for line in orig_chgui:
                data = line.split('|')
                new_data = []
                for i in range(0, len(data)):
                    if i == 1:
                        name = data[i]
                        ename = name[name.index('(')+1:name.index(')')-1]
                        new_data.append(ename)
                    elif i in (7, 9, 11):
                        # important data, * 100
                        # 命中/出手
                        chushou_mingzhong = data[i].split('-')
                        chushou = chushou_mingzhong[0]
                        mingzhong = chushou_mingzhong[1]
                        new_data.append(chushou)
                        new_data.append(mingzhong)
                    else:
                        new_data.append(data[i])
                new_chgui.write("|".join(new_data))


def clean_info(info_file_path, new_file_path):
    """
    0: ID	1: name	2: 个人网址	3: 个人头像	4: 身高	5: 位置
    6: 体重	7: 生日	8: 球队	9: 学校	10: 选秀
    11: 出生地	12: 本赛季薪金	13: 合同	14: 常规赛参加情况	15: 季后赛参加情况
    :param info_file_path:
    :return:
    """
    title_info = 'ID|name|website|profile|heigh|position|weight|birth|team|school|xuanxiu|born|salary|contract|regular race|season race'
    with open(new_file_path, mode='w') as new_info:
        with open(info_file_path) as orig_info:
            new_info.write(title_info + os.linesep)
            orig_info.readline()
            for line in orig_info:
                data = line.split('|')
                new_data = []
                for i in range(0, len(data)):
                    if i == 1:
                        name = data[i]
                        ename = name[name.index('(')+1:name.index(')')-1]
                        new_data.append(ename)
                    elif i == 4:
                        # using meter
                        heigh = data[i]
                        new_heigh = data[i][:data[i].index('米')] #米
                        new_data.append(new_heigh)
                    elif i == 5:
                        pos = data[i][:data[i].index('(')] #F/C(33号)
                        new_data.append(pos)
                    elif i == 6:
                        # using kg
                        weight = data[i]
                        new_weight = data[i][:data[i].index('公斤')] #公斤
                        new_data.append(new_weight)
                    elif i == 7:
                        # convert birth to month
                        dt = datetime.datetime.strptime(data[i], "%Y-%m-%d")
                        new_birth = (datetime.datetime.now().year - dt.year) * 12 + (datetime.datetime.now().month - dt.month)
                        new_data.append(str(new_birth))
                    elif i == 12:
                        # using x*10k dollar per year
                        salary = data[i].strip()
                        if salary:
                            new_salary = data[i][:data[i].index('万美元')].strip() #万美元
                            if new_salary:
                                new_data.append(new_salary)
                            else:
                                new_data.append('0')
                        else:
                            new_data.append('0')
                    else:
                        new_data.append(data[i])
                new_info.write("|".join(new_data))


def parse_info(info_file):
    # 0: ID	1: name	2: 个人网址	3: 个人头像	4: 身高	5: 位置
    # 6: 体重	7: 生日	8: 球队	9: 学校	10: 选秀
    # 11: 出生地	12: 本赛季薪金	13: 合同	14: 常规赛参加情况	15: 季后赛参加情况
    f = open(info_file)
    f.readline()
    info = {}
    for line in f:
        fields = line.split('|')
        fields[5] = fields[5][:fields[5].index('(')] # PG(8号)
        info[fields[0]] = fields[1:]
    return info


def try_convert_int(s):
    """
    try convert s to int, if failed, return s itself
    :param s:
    :return:
    """
    new_obj = s
    try:
        if s.strip().index('%'):
            new_obj = s.strip('% ')
        new_obj = int(s)
    except:
        new_obj = s
    return new_obj

def merge_race_info_by_id(race_file):
    # 0: ID	1: name	2: 赛季	3: 球队	4: 场次	5: 首发
    # 6: 时间	7: 投篮命中	8: 投篮出手	9: 命中率	10: 三分命中
    # 11: 三分得手	12: 命中率	13: 罚球命中	14: 罚球出手	15: 命中率
    # 16: 篮板	17: 助攻	18: 抢断	19: 盖帽	20: 失误
    # 21: 犯规	22: 得分
    #10001|Tony Parke|2001|马刺|77|72|29.4|3.5|8.3|41.9%|0.8|2.5|32.3%|1.4|2.1|67.5%|2.6|4.3|1.16|0.09|1.96|2.16|9.2
    f = open(race_file)
    f.readline()
    race_info = {}
    for line in f:
        try:
            fields = line.split("|")
            id = fields[0]
            first_race_info = False
            if id in race_info:
                first_race_info = True
            num_fields = map(try_convert_int, fields[4:])
            num_fields.insert(0, fields[3])
            num_fields.insert(0, fields[2])
            num_fields.insert(0, fields[1])
        except:
            print("error while parsing: " + line)
            raise




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--printgbk", help="print gpk encoding file")
    parser.add_argument("--race_file", help="clean jihou file")
    parser.add_argument("--info_file", help="clean changgui file")
    parser.add_argument("--new_file", help="write data to new file")
    args = parser.parse_args()
    if args.printgbk:
        print_gbk_str(args.printgbk)
    elif args.race_file and args.new_file:
        clean_chgui(args.race_file, args.new_file)
    elif args.info_file and args.new_file:
        clean_info(args.info_file, args.new_file)
    else:
        parser.print_usage()


if __name__ == "__main__":
    main()

