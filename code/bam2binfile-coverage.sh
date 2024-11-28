#!/bin/bash

# 设置输入 BAM 文件目录和输出目录
BAM_DIR="/cluster/facility/yzhang/WorkSpace/CUT-Tag/20240819_WXD/mapped-bam-shx"
OUTPUT_DIR="/cluster/facility/yzhang/WorkSpace/CUT-Tag/20240819_WXD/coverage-bin5000-non-dedup-shx"
# BINS_FILE="/cluster/facility/yzhang/WorkSpace/CUT-Tag/20240819_WXD/mm10_bins_1000000.bed"
BINS_FILE="/cluster/facility/yzhang/WorkSpace/CUT-Tag/20240819_WXD/mm10_bins_5000.sorted.bed"
NUM_THREADS=8  # 并行处理的线程数量

# 创建输出目录（如果不存在）
mkdir -p "$OUTPUT_DIR"

# 处理 BAM 文件的函数
process_bam() {
    local BAM_FILE=$1
    local BAM_BASENAME=$(basename "$BAM_FILE" .bam)
    
    # 使用 bamCoverage 生成覆盖率 bedGraph 文件
    bamCoverage -b "$BAM_FILE" \
                -o "${OUTPUT_DIR}/${BAM_BASENAME}.bdg" \
                --outFileFormat bedgraph \
                --binSize 10000 \
                -p 8
    echo finished
    # 使用 bedtools intersect 将 bamCoverage 结果与固定 bins 文件对齐，并提取指定列
    # bedtools intersect -a "$BINS_FILE" -b "${OUTPUT_DIR}/${BAM_BASENAME}.bdg" -wa -wb | \
    # awk '{print $1, $2, $3, $7}' OFS='\t' > "${OUTPUT_DIR}/${BAM_BASENAME}_aligned.bdg"
    sort -k1,1 -k2,2n "${OUTPUT_DIR}/${BAM_BASENAME}.bdg" -o "${OUTPUT_DIR}/${BAM_BASENAME}.1bdg"
    bedtools map -a "$BINS_FILE" -b "${OUTPUT_DIR}/${BAM_BASENAME}.1bdg" -c 4 -o sum | \
    awk '{print $1, $2, $3, ($4 == "." ? 0 : $4)}' OFS='\t' > "${OUTPUT_DIR}/${BAM_BASENAME}_aligned.bdg"
    echo "$BAM_FILE processing complete."
}

# 导出函数和变量，以便子进程能够访问
export -f process_bam
export BAM_DIR OUTPUT_DIR BINS_FILE

# 遍历 BAM 文件目录中的所有 BAM 文件，并进行并行处理
find "$BAM_DIR" -name "*.bam" | xargs -n 1 -P $NUM_THREADS -I {} bash -c 'process_bam "$@"' _ {}

echo "Coverage calculation and alignment complete for all BAM files."
