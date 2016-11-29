#!/usr/bin/python
#coding:utf-8
import os



def clean_chgui():
    title_race = 'ID|name|season|team|changci|shoufa|time|toulan_chusou|toulan_mingzhong|mingzhonglv|3fen_chushou|3fen_mingzhong|3fenmingzhong|faqiu_total|faqiu_mingzhong|faqiu_mingzhonglv|lanban|zhugong|qiangduan|gaimao|shiwu|fangui|defen'
    with open('nba_chgui_clean.txt', mode='w') as new_chgui:
        with open('nba_chgui.txt', mode='r') as orig_chgui:
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

def clean_info():
    title_info = 'ID|name|website|profile|heigh|position|weight|birth|team|school|xuanxiu|born|salary|contract|regular race|season race'
    with open('nba_info_clean.txt',mode='w') as new_info:
        with open('nba_info.txt') as orig_info:
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
                        new_heigh = data[i][:data[i].index('\xc3\xd7')-1] #米
                        new_data.append(new_heigh)
                    elif i == 6:
                        weight = data[i]
                        new_weight = data[i][:data[i].index('\xb9\xab\xbd')-1] #公斤
                        new_data.append(new_weight)
                    elif i == 12:
                        salary = data[i]
                        if salary:
                            new_salary = data[i][:data[i].index('\xcd\xf2')-1] #万美元
                            new_data.append(new_salary)
                        else:
                            new_data.append(salary)
                    else:
                        new_data.append(data[i])
                new_info.write("|".join(new_data))


if __name__=="__main__":

    clean_chgui()
    clean_info()

