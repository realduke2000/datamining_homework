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


def clean_chgui(race_file):
    title_race = 'ID|name|season|team|changci|shoufa|time|toulan_chusou|toulan_mingzhong|mingzhonglv|3fen_chushou|3fen_mingzhong|3fenmingzhong|faqiu_total|faqiu_mingzhong|faqiu_mingzhonglv|lanban|zhugong|qiangduan|gaimao|shiwu|fangui|defen'
    with open('%s.clean' % race_file, mode='w') as new_chgui:
        with open(race_file, mode='r') as orig_chgui:
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
                    elif i == 7 or i == 9 or i == 11:
                        chushou_mingzhong = data[i].split('-')
                        chushou = chushou_mingzhong[0]
                        mingzhong = chushou_mingzhong[1]
                        new_data.append(chushou)
                        new_data.append(mingzhong)
                    else:
                        new_data.append(data[i])
                new_chgui.write("|".join(new_data))


def clean_info(info_file):
    title_info = 'ID|name|website|profile|heigh|position|weight|birth|team|school|xuanxiu|born|salary|contract|regular race|season race'
    with open('%s.clean' % info_file,mode='w') as new_info:
        with open(info_file) as orig_info:
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
                        heigh = data[i]
                        new_heigh = data[i][:data[i].index('米')-1] #米
                        new_data.append(new_heigh)
                    elif i == 6:
                        weight = data[i]
                        new_weight = data[i][:data[i].index('公斤')-1] #公斤
                        new_data.append(new_weight)
                    elif i == 7:
                        dt = datetime.datetime.strptime(data[i], "%Y-%m-%d")
                        new_birth = time.mktime(dt.timetuple())
                        new_data.append(str(new_birth))
                    elif i == 12:
                        salary = data[i].strip()
                        if salary:
                            new_salary = data[i][:data[i].index('万美元')-1].strip() #万美元
                            if new_salary:
                                new_data.append(new_salary)
                            else:
                                new_data.append('0')

                        else:
                            new_data.append('0')
                    else:
                        new_data.append(data[i])
                new_info.write("|".join(new_data))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--printgbk", help="print gpk encoding file")
    parser.add_argument("--race_file", help="clean jihou file")
    parser.add_argument("--info_file", help="clean changgui file")
    args = parser.parse_args()
    if args.printgbk:
        print_gbk_str(args.printgbk)
    elif args.race_file:
        clean_chgui(args.race_file)
    elif args.info_file:
        clean_info(args.info_file)


if __name__ == "__main__":
    main()

