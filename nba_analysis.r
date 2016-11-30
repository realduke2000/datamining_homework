

dir = "/home/allenh/src/github/datamining_homework"

info<-read.csv(stringr::str_c(dir, "/nba_info_utf8.txt.clean"),sep = '|')
mini_info <- info[,c(5,7,8,13,15,16)]
#jihou<-read.csv(stringr::str_c(dir, "/nba_jihou.txt"),sep = '|')
#chgui<-read.csv(stringr::str_c(dir, "/nba_chgui_clean.txt"),sep = '|')

#data=merge(info,chgui, by.x = 'ID', by.y = 'ID')

cl = kmeans(mini_info, 10)

plot(mini_info, col=cl$cluster)
