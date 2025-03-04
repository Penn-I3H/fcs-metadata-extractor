library(flowCore)
library(stringr)

dir_in <- Sys.getenv("INPUT_DIR")
dir_out <- Sys.getenv("OUTPUT_DIR")

# dir_in <- "~/Documents/git/R/allcytof/data/balanced/"

### list all available FCS files
files <- list.files(dir_in, pattern=".fcs")
file <- files[1]

### read headers and extract columns of interest
cols <- c("$BTIM", "$ETIM", "$DATE", "$TOT",
          "Comment", "TotalSampleVolume", "CellCount")

df_list <- lapply(files, function(file) {
  path <- paste0(dir_in, "/", file)
  print("file")
  print(file)
  header <- read.FCSheader(path, emptyValue=FALSE)[[1]]
  print("hello2")
  df <- as.data.frame(t(as.matrix(header[cols])))
  
  df["$TOT"] <- as.integer(df["$TOT"]) # remove trailing zeros
  if ("Comment" %in% colnames(df))
  {
    df$Comment <- str_replace(df$Comment, "/", "_")
  } else {
    df[, 'Comment'] <- "NA"
    df <- df[!is.na(names(df))]
  }
  df$File <- file # add file name
  print(df)
  
  return(df)
})

df_meta <- do.call(rbind, df_list)
write.csv(df_meta, file=paste0(dir_out, "/fcs_metadata.csv"), row.names = FALSE)
