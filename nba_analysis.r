
info<-read.csv("/Users/houhualong/Developer/src/bigdata/nba/nba_info_clean.txt",sep = '|')
#jihou<-read.csv("/Users/houhualong/Developer/src/bigdata/nba/nba_jihou.txt",sep = '|')
chgui<-read.csv("/Users/houhualong/Developer/src/bigdata/nba/nba_chgui_clean.txt",sep = '|')

data=merge(info,chgui, by.x = 'ID', by.y = 'ID')
