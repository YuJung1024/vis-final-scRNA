#!/usr/bin/env Rscript

library(Seurat)
library(Matrix)

base_dir <- "../../.././"               # 從 rscripts/ 出發回到 DESC
data_root <- file.path(base_dir, "GSE161340")

# 小工具：讀一個 10x 資料夾，變成 Seurat 物件並加 metadata
read_one_10x <- function(subdir, group, condition, replicate, data_type) {
  folder <- file.path(data_root, subdir)
  cat("Reading", folder, "\n")

  mtx <- Read10X(folder)    # 如果是 feature_name 為 gene symbol，就 OK
  obj <- CreateSeuratObject(counts = mtx, project = "GSE161340")

  obj$group      <- group
  obj$condition  <- condition
  obj$replicate  <- replicate
  obj$data_type  <- data_type
  obj$sample_id  <- subdir

  return(obj)
}

objs <- list(
  # 自然衰老組：sn
  read_one_10x("sn_OBrain1_mm10_pre_mRNA", "自然衰老", "年老",   1, "sn"),
  read_one_10x("sn_OBrain3_mm10_pre_mRNA", "自然衰老", "年老",   2, "sn"),
  read_one_10x("sn_YBrain1_mm10_pre_mRNA", "自然衰老", "年輕",   1, "sn"),
  read_one_10x("sn_YBrain3_mm10_pre_mRNA", "自然衰老", "年輕",   2, "sn"),

  # 清除衰老細胞治療組：sc
  read_one_10x("sc_OBrain1_mm10",          "清除衰老細胞", "年老", 1, "sc"),
  read_one_10x("sc_OBrain3_mm10",          "清除衰老細胞", "年老", 2, "sc"),
  read_one_10x("sc_YBrain1_mm10",          "清除衰老細胞", "年輕", 1, "sc"),
  read_one_10x("sc_YBrain3_mm10",          "清除衰老細胞", "年輕", 2, "sc")
)

# merge 成一個 object
pbmc <- objs[[1]]
if (length(objs) > 1) {
  for (i in 2:length(objs)) {
    pbmc <- merge(pbmc, y = objs[[i]])
  }
}

cat("Merged object cells:", ncol(pbmc), "genes:", nrow(pbmc), "\n")

# 基本前處理（你之後可以調整這些 cutoff）
pbmc[["percent.mt"]] <- PercentageFeatureSet(pbmc, pattern = "^mt-")

pbmc <- subset(pbmc,
               subset = nFeature_RNA > 500 &
                        nFeature_RNA < 6000 &
                        percent.mt < 10)

pbmc <- NormalizeData(pbmc)
pbmc <- FindVariableFeatures(pbmc, selection.method = "vst", nfeatures = 2000)
pbmc <- ScaleData(pbmc, features = VariableFeatures(pbmc))

# 預先做 30 維 PCA（跟原本 paper 類似）
pbmc <- RunPCA(pbmc, npcs = 30, verbose = FALSE)

# 建立 rds/ 資料夾
rds_dir <- file.path(base_dir, "codes", "rscripts", "rds")
if (!dir.exists(rds_dir)) dir.create(rds_dir, recursive = TRUE)

# rds 檔名：「你等等要在 analysis.html 裡指定的 rds_name」
rds_name <- "GSE161340_merged.rds"
save_path <- file.path(rds_dir, rds_name)

saveRDS(pbmc, file = save_path)
cat("Saved Seurat object to:", save_path, "\n")
