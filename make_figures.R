library(tidyverse)
source("utils.R")
Rcpp::sourceCpp("js.cpp")

### input and output directories, modify as necessary
study <- "ISPY"
dir_in <- "../../R/allcytof/AnalysisResultsAug2024/"
dir_out <- "figures/"

dir.create(paste0(dir_out, "QC_all"))
dir.create(paste0(dir_out, "QC_controls"))


### read file containing metadata for cohort of interest
path_to_meta <- "metadata.csv"
meta <- read_csv(path_to_meta) 

### select metadata column to highlight in plots 
### (later we could pass as parameter)
col <- "Visit"


### assemble table of all features present in input dirs
files_ada <- list.files(dir_in, pattern="feat_adaptive", recursive = TRUE)
files_maj <- str_replace_all(files_ada, "adaptive", "major")

df_feat_list <- Map(read_features, 
                    paste0(dir_in, files_ada), 
                    paste0(dir_in, files_maj)) 

df_feat <- df_feat_list %>%
  do.call(what=plyr::rbind.fill) %>%
  as_tibble() %>%
  select(!matches("out of")) %>%
  replace(is.na(.), 0)

feat_names <- names(df_feat %>% select(-file))
  

### build umap dimensional reduction
set.seed(0)
mat <- df_feat %>% select(where(is.numeric)) %>% as.matrix() %>% scale()
um <- uwot::umap(mat, min_dist = 0.2, n_neighbors = 7)

df_feat_aug <- df_feat %>%
  mutate(umap1 = um[,1], umap2 = um[,2]) %>%
  left_join(meta)


### make and save plots

p <- plot_umap_color_metadata(df_feat_aug, col = col)
ggsave(p, filename=paste0(dir_out, "/umap.png"), width=12, height=9)

p <- plot_box(df_feat_aug, feat_names, col)
ggsave(p, filename=paste0(dir_out, "/boxplots.png"), width=12, height=9)

p <- plot_lasso(df_feat_aug, feat_names, col)
ggsave(p, filename=paste0(dir_out, "/lasso.png"), width=12, height=4)



### cleanup stats

files_stats <- list.files(paste0(dir_in,"ISPY"), 
                          pattern="cleanup_stats", 
                          recursive = TRUE)

df_stats <- lapply(paste0(dir_in, "ISPY/", files_stats), function(path) {
  read_csv(path, col_types = cols(), progress=FALSE)
}) %>% do.call(what=rbind)

p <- plot_cleanup_stats(df_stats)
ggsave(p, filename=paste0(dir_out, "/cleanup.png"), width=12, height=9)




### QC plots based on density estimates across all channels

files_kde <- list.files(paste0(dir_in, "/", study, "/kdes_for_qc/"), pattern=".csv")
paths_kde <- paste0(dir_in, "/", study, "/kdes_for_qc/", files_kde)

df_kde <- lapply(paths_kde, read_csv, col_types=cols()) %>%
  do.call(what=rbind)

cell_types <- c("Neutrophil", "B cell", "T cell CD4", "T cell CD8")

# all files in the study

js_scores <- lapply(cell_types, run_cell_type_js, 
                    df_kde=df_kde, dir_out=paste0(dir_out, "/QC_all/"),
                    n_sd_cutoff=1.5, min_cutoff=0.1) %>%
  Reduce(f=full_join)

plot_js_across_cell_types(js_scores, dir_out=paste0(dir_out, "/QC_all/"))

write_csv(js_scores, file=paste0(dir_out, "js_scores.csv"))


# just the technical controls

js_scores <- lapply(cell_types, run_cell_type_js, 
                    df_kde=df_kde %>% filter(grepl("HD", file)), 
                    dir_out=paste0(dir_out, "/QC_controls/"),
                    n_sd_cutoff=1.5, min_cutoff=0.1) %>%
  Reduce(f=full_join) 

plot_js_across_cell_types(js_scores, dir_out=paste0(dir_out, "/QC_controls/"))





