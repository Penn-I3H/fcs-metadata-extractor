library(flowCore)

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
  header <- read.FCSheader(path)[[1]]
  df <- as.data.frame(t(as.matrix(header[cols])))
  
  df["$TOT"] <- as.integer(df["$TOT"]) # remove trailing zeros
  df$File <- file # add file name
  
  return(df)
})

df_meta <- do.call(rbind, df_list)
write.csv(df_meta, file=paste0(dir_out, "/fcs_metadata.csv"), row.names = FALSE)
