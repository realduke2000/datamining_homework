#setwd("C:\\Users\\305032239\\Documents\\Master\\多元统计分析与R语言建模\\作业")
setwd('/home/allenh/src/github/datamining_homework/football_player')
brazil_players = read.csv("brazil.csv",header=T)#读入数据
brazil_players= na.omit(brazil_players[,c(16,19:21, 26:33, 36:49)]) #选择部分变量，删除有缺失数据的行
brazil_players[1,]#浏览数据的第一行
library(e1071)
library(rpart)
library(mlbench)
brazil_players$Best.Position=as.factor(brazil_players$Best.Position)#转化成字符型
index = 1:nrow(brazil_players)#nrow(customer)表示customer的行数
testindex = sample(index, trunc(length(index)/3))#测试集的行号，从index中抽取约1/3的样本，trunc()向零取整
testset = brazil_players[testindex, ]#testset测试集
trainset = brazil_players[-testindex, ]#trainset训练集
svm.model = svm(trainset$Best.Position ~ ., data = trainset, cost = 100, gamma = 1e-04, cross=10)#支持向量机，用训练集训练模型
svm.pred = predict(svm.model, testset[, -1])#用svm.model模型，testset[, -37]数据预测,
summary(svm.model)
table(pred = svm.pred, true = testset[, 1])#预测结果与真实值列表，支持向量机的预测效果


#将支持向量机算法与分类树算法进行比较：
rpart.model = rpart(trainset$Best.Position ~ ., data = trainset)#分类树算法，数据为训练集
summary(rpart.model)
rpart.pred = predict(rpart.model, testset[, -1], type = "class")#预测，预测结果为字符型
table(pred = svm.pred, true = testset[, 1])#预测结果与真实值列表，支持向量机的预测效果
table(pred = rpart.pred, true = testset[, 1])#预测结果与真实值列表，分类树的预测效果







#非线性核函数支持向量机算法如下：
#customer  =  read.csv("customer.csv",header=T)#读入数据
#customer  =  na.omit(customer[,c(1:11,16:40,42)]) #选择部分变量，删除有缺失数据的行
#customer[1,]#浏览数据的第一行
#customer$churn=as.factor(customer$churn)#转化成字符型
#library(e1071);library(rpart)
#index = 1:nrow(brazil_players)#nrow(customer)表示customer的行数
#testindex = sample(index, trunc(length(index)/3))#测试集的行号，从index中抽取约1/3的样本，trunc()向零取整
#testset = customer[testindex,]#testset测试集
#trainset = customer[-testindex,]#trainset训练集
svm.model = svm(trainset$Best.Position~., data = trainset, cost = 100, gamma = 1e-04)
#支持向量机，用训练集训练模型
svm.pred = predict(svm.model, testset[, -1])#用svm.model模型，testset[, -37]数据预测
table(pred = svm.pred, true = testset[, 1])#预测结果与真实值列表，支持向量机的预测效果

crossprod(as.numeric(svm.pred)-as.numeric(testset[,1]))/length(testindex)#交叉验证
rpart.model = rpart(trainset$Best.Position ~ ., data = trainset)
rpart.pred = predict(rpart.model, testset[, -1], type="class")
crossprod(as.numeric(rpart.pred)-as.numeric(testset[,1]))/length(testindex)#交叉验证

sum((as.numeric(svm.pred)-as.numeric(testset[,1]))==0)
sum((as.numeric(rpart.pred)-as.numeric(testset[,1]))==0)


