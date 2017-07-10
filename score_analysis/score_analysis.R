library(readr)
library(reshape)
library(sqldf)
setwd('/home/allenh/src/github/datamining_homework/score_analysis')
#setwd('~/Developer/src/github/datamining_homework/score_analysis')

merge_data <- function(filename, ncols) {
  scores <- read_delim(
    paste("./scores/csv/", filename, sep = ""),
    "\t",
    escape_double = FALSE,
    trim_ws = TRUE
  )
  scores <- scores[, c(ncols)]
  fields <- strsplit(filename, "\\.")
  scores$type <- factor(unlist(fields)[3])
  scores$date <-
    as.Date(paste(unlist(fields)[1], unlist(fields)[2], "01"), format = "%Y %m %d")
  return(scores)
}


data <-
  read_csv(
    "scores/scores.csv",
    col_types = cols(
       Biology = col_number(),
       Geo = col_number(),
       History = col_number(),
       Moral = col_number(),
       Physics = col_number(),
       Math = col_number(),
       Oral = col_number(),
       English = col_number(),
       Chinese = col_number(),
      class = col_factor(levels = c("1", "2", "3", "4")),
      date = col_date(format = "%Y-%m-%d"),
      type = col_factor(levels = c("monthly",
                                   "mid", "end"))
    )
  )

summary(data)

draw_lm <- function(data, stuid) {
  sample_students <- subset(data, id == stuid)
  sample_students <- sample_students[order(sample_students$date), ]
  
  attach(sample_students)
  par(mfrow = c(2, 2))
  
  plot(
    range(as.Date('2015-06-01'), as.Date('2018-01-01')),
    range(0, 100),
    type = 'n',
    xlab = "Date",
    ylab = "Math"
  )
  lines(date, Math, type = 'b', col = 'red')
  
  plot(
    range(as.Date('2015-06-01'), as.Date('2018-01-01')),
    range(0, 100),
    type = 'n',
    xlab = "Date",
    ylab = "Chinese"
  )
  lines(date, Chinese, type = 'b', col = 'blue')
  
  plot(
    range(as.Date('2015-06-01'), as.Date('2018-01-01')),
    range(0, 100),
    type = 'n',
    xlab = "Date",
    ylab = "English"
  )
  lines(date, English, type = 'b')
  
  plot(
    range(as.Date('2015-06-01'), as.Date('2018-01-01')),
    range(0, 100),
    type = 'n',
    xlab = "Date",
    ylab = "Scores"
  )
  lines(date, Math, type = 'p', col = 'red')
  lines(date, Chinese, type = 'p', col = 'blue')
  lines(date, English, type = 'p')
  detach(sample_students)
}

#draw_lm(data, 920150425)


test_cluster <- function(data) {
  test_data <- data[, c(3, 13, 18)]
  test_data <- na.omit(test_data)
  summary(test_data)
  cl = kmeans(test_data, 3)
  plot(test_data, cl$cluster)
}

range_sort <- function(data, stuid) {
  new_data <-
    data[, c("id", "name", "date", "Math", "Chinese", 'English')]
  new_data <- na.omit(new_data)
  new_data <-
    transform(new_data, Score = new_data$Chinese + new_data$Math + new_data$English)
  dates <- sqldf("select distinct(date) from new_data")
  
  stuindexes = new_data[0, c('id', 'name', 'date', 'Score')]
  for (i in 1:nrow(dates)) {
    curr_exam = dates[i, ]
    one_exame_scores <- new_data[which(new_data$date == curr_exam), ]
    one_exame_scores <-
      one_exame_scores[order(one_exame_scores$Score, decreasing = TRUE), ]
    row_count = nrow(one_exame_scores)
    one_exame_scores <-
      transform(one_exame_scores, index = 1:row_count)
    stuindex = one_exame_scores[which(one_exame_scores$id == stuid), c('id', 'date', 'name', 'index')]
    stuindexes <- rbind(stuindexes, stuindex)
  }
  stuindexes <- stuindexes[order(stuindexes$date), ]
  stu_name = stuindexes[1,c('name')]
  png(filename = paste("rank_trend",stu_name,".png"))
  opar <- par(no.readonly = TRUE)
  plot(
    xlab = "Date",
    ylab = "Rank",
    x=stuindexes$date,
    y=stuindexes$index,
    type = 'b',
    axes=FALSE,
    ylim = c(100,1)
  )
  #lines(stuindexes$date, stuindexes$index, type = 'b')
  text(stuindexes$date, stuindexes$index + 3, stuindexes$index, cex = 0.8)
  #text(stuindexes$date+3, stuindexes$index, stuindexes$date, cex = 0.8)
  axis(side = 1, at=stuindexes$date, labels = stuindexes$date)
  axis(side = 2)
  title(stu_name)
  par(opar)
  dev.off()
}
create_all_rank_trend <- function(){
  ids <- sqldf("select distinct id from data")
  for (i in 1:nrow(ids)){
    curr_id = ids[i,]
    range_sort(data, curr_id)
  }
}

create_all_rank_trend()