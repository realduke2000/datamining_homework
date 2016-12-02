
#dir = "/home/allenh/src/github/datamining_homework"
dir = "/Users/houhualong/Developer/src/bigdata/nba"

info<-read.csv(stringr::str_c(dir, "/resources/nba_info.clean.txt"),sep = '|')
jihou<-read.csv(stringr::str_c(dir, "/resources/nba_jihou.clean.txt"),sep = '|')
chgui<-read.csv(stringr::str_c(dir, "/resources/nba_chgui.clean.txt"),sep = '|')

# info
#0: ID	1: name	2: 个人网址	3: 个人头像	4: 身高	5: 位置
#6: 体重	7: 生日	8: 球队	9: 学校	10: 选秀
#11: 出生地	12: 本赛季薪金	13: 合同	14: 常规赛参加情况	15: 季后赛参加情况


cluster_info <- function ()
{
  mini_info <- info[,c(5,7,8,13,15,16)]
  cl = kmeans(mini_info, 10)

  plot(mini_info, col=cl$cluster)
  return
}

# race
#0: ID	1: name	2: 赛季	3: 球队	4: 场次	5: 首发
#6: 时间	7: 投篮命中	8: 投篮出手	9: 命中率	10: 三分命中
#11: 三分得手	12: 命中率	13: 罚球命中	14: 罚球出手	15: 命中率
#16: 篮板	17: 助攻	18: 抢断	19: 盖帽	20: 失误
#21: 犯规	22: 得分

cluster_jihou_race <-function()
{
  new_jihou <- jihou[which(jihou[,3]==2013),]
  new_data <- merge(new_jihou, info, by.x = "ID", by.y = "ID")
  new_data <- new_data[,c(17:23)]
  new_data <- na.omit(new_data)
  cl = kmeans(new_data, 5)
  plot(new_data, col=cl$cluster)
}

cluster_chgui_race <-function()
{
  new_chgui <- chgui[which(chgui[,3]==2013),]
  new_data <- merge(new_chgui, info, by.x = "ID", by.y = "ID")
  new_data <- new_data[,c(8,11,14,17:22)]
  new_data <- na.omit(new_data)
  cl = kmeans(new_data, 5)
  plot(new_data, col=cl$cluster)
  #A[order(A[,4],decreasing=T),] ＃按照第4列降序排序
  #失误，三分，助攻
}


svm_player <- function()
{
  library(e1071)
  library(rpart)
  library(mlbench)
  
  cg_player<-sqldf("select * from info where position = 'C' or position = 'G' or position = 'SG' or position = 'PG'")
  new_chgui <- chgui[which(chgui[,3]==2013),]
  cg_data <- merge(new_chgui, cg_player, by.x = "ID", by.y = "ID")
  train_data <- cg_data[,c(11,12,17,19,20,22,27,29)]
  cl = kmeans(train_data, 2)
  plot(train_data, col=cl$cluster)
  svm.model = svm(churn ~ ., data = train_data, cost = 100, gamma = 2)
  
}


