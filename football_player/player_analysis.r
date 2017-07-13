library(readr)
library(reshape)
library(sqldf)
library(psych)

#setwd('/home/allenh/src/github/datamining_homework/')
setwd('/Users/houhualong/Developer/src/github/datamining_homework')

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

player.cluster <- function() {
  alb <- read.csv('football_player/Albania.csv')
  brz <- read.csv('football_player/brazil.csv')
  names(alb)
  names(brz)
  alb.features <- select.feature(alb)
  brz.features <- select.feature(brz)
  players <- rbind(alb.features, brz.features)
  players <- na.omit(players)
  kmeans.model <- kmeans(players[, c(-1,-2)], 2)
  par(mfrow=c(1,1))
  
  plot(players[, c('Nationality')], col = kmeans.model$cluster)
  #plot(players[, c('LongPass', 'Nationality')], col = kmeans.model$cluster)
}

#
# from player capabilities clustering, we can observe that the player of Brazil
# is obviously better that Albania(Algeria)
#
player.cluster()

player.means <- function() {
  alb <- read.csv('football_player/Albania.csv')
  brz <- read.csv('football_player/brazil.csv')
  alb.features <- select.feature(alb)
  brz.features <- select.feature(brz)
  alb.features <- na.omit(alb.features)
  alb.features$Nationality <- 'Albania'
  brz.features <- na.omit(brz.features)
  features <- rbind(alb.features, brz.features)
  
  means <-
    aggregate(features,
              by = list(features$Nationality),
              FUN = mean)
  par(mfrow = c(2, 3))
  barplot(means$Attack,
          names.arg = means$Group.1,
          ylab = 'Attack')
  barplot(means$Defend,
          names.arg = means$Group.1,
          ylab = 'Defend')
  barplot(means$Speed,
          names.arg = means$Group.1,
          ylab = 'Speed')
  barplot(means$Reaction,
          names.arg = means$Group.1,
          ylab = 'Reaction')
  
  barplot(means$Reaction,
          names.arg = means$Group.1,
          ylab = 'Marking.')
  
  barplot(means$Reaction,
          names.arg = means$Group.1,
          ylab = 'Technique')
  
  alb.var <- apply(alb.features[,c(-1,-2)], MARGIN = 1, FUN = var)
  brz.var <- apply(brz.features[,c(-1,-2)], MARGIN = 1, FUN = var)
  print(mean(alb.var))
  print(mean(brz.var))
}

player.means()
