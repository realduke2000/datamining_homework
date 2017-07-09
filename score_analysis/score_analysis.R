merge_data <- function(filename, ncols) {
  library(readr)
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

setwd('~/Developer/src/R/score_analysis')
data <- read.csv(file = "./scores/scores.csv")
