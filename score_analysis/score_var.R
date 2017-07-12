library(readr)
library(reshape)
library(sqldf)
setwd('/home/allenh/src/github/datamining_homework/score_analysis')
#setwd('~/Developer/src/github/datamining_homework/score_analysis')
read_scores <- function() {
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
  return(data)
}
