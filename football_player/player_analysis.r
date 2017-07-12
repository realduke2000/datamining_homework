library(readr)
library(reshape)
library(sqldf)

setwd('/home/allenh/src/github/datamining_homework/')
alb <- read.csv('football_player/Albania.csv')
brz <- read.csv('football_player/brazil.csv')
names(alb)
names(brz)


select.feature <- function(data) {
  featured.data <-
    data[, c(
      "Real.Name",
      'Nationality',
      'Defend',
      "Attack",
      "Power",
      "Speed",
      'Reaction',
      'Technique',
      'Team.Work',
      'Dribble.',
      'Jumping.',
      'Tackling.',
      'LongPass',
      'Marking.'
    )]
  return(featured.data)
}

alb.features <- select.feature(alb)
brz.features <- select.feature(brz)
players <- rbind(alb.features, brz.features)
players <- na.omit(players)
kmeans.model <- kmeans(players[,c(-1,-2)], 2)
plot(players[,c('Nationality')], col=kmeans.model$cluster)