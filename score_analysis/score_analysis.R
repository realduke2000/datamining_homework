library(readr)
library(reshape)
setwd('/home/allenh/src/github/datamining_homework/score_analysis')

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
      Biology = col_integer(),
      Geo = col_integer(),
      History = col_integer(),
      Moral = col_integer(),
      Physics = col_integer(),
      class = col_factor(levels = c("1",
                                    "2", "3", "4")),
      date = col_date(format = "%Y-%m-%d"),
      type = col_factor(levels = c("monthly",
                                   "mid", "end"))
    )
  )

summary(data)

draw_lm <- function(data, stuid) {
  sample_students <- subset(data, id == stuid)
  sample_students <- sample_students[order(sample_students$date),]
  
  attach(sample_students)
  par(mfrow=c(2,2))
  
  plot(range(as.Date('2015-06-01'),as.Date('2018-01-01')),range(0,100),type='n', xlab = "Date", ylab="Math")
  lines(date, Math, type='b', col='red')
  
  plot(range(as.Date('2015-06-01'),as.Date('2018-01-01')),range(0,100),type='n', xlab = "Date", ylab="Chinese")
  lines(date, Chinese, type='b', col='blue')
  
  plot(range(as.Date('2015-06-01'),as.Date('2018-01-01')),range(0,100),type='n', xlab = "Date", ylab="English")
  lines(date, English, type='b')
  
  plot(range(as.Date('2015-06-01'),as.Date('2018-01-01')),range(0,100),type='n', xlab = "Date", ylab="Scores")
  lines(date, Math, type='p', col='red')
  lines(date, Chinese, type='p', col='blue')
  lines(date, English, type='p')
  detach(sample_students)
}

draw_lm(data, 920150425)


test_cluster <- function(data) {
  test_data <- data[, c(3, 13, 18)]
  test_data <- na.omit(test_data)
  summary(test_data)
  cl = kmeans(test_data, 3)
  plot(test_data, cl$cluster)
}
