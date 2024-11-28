#!/bin/bash

# 指定包含 BAM 文件的文件夹
input_folder="/cluster/facility/yzhang/WorkSpace/CUT-Tag/20240819_WXD/mapped-bam"
output_folder="/cluster/facility/yzhang/WorkSpace/CUT-Tag/20240819_WXD/mapped-bam-shx"

# 创建输出文件夹（如果不存在）
mkdir -p "$output_folder"

# 遍历文件夹中的所有 BAM 文件
for bam_file in "$input_folder"/*.bam; do
    # 获取文件名，不包含路径
    filename=$(basename "$bam_file")
    
    # 输出文件名
    temp_file="$output_folder/temp_${filename}"
    output_file="$output_folder/mapped_${filename}"
    
    # 使用 samtools 过滤未映射的 reads
    samtools view -t 3 -b -F 4 "$bam_file"  > "$temp_file"

    samtools sort -@ 3 -o "$output_file" "$temp_file"
    # 创建索引（可选）
    samtools index "$output_file"
    
    echo "Processed: $bam_file -> $output_file"
done

echo "All BAM files have been processed."