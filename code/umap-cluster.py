import os
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import umap
import matplotlib.pyplot as plt
import seaborn as sns


# 文件夹路径
folder_path = 'Path_to_coverage_bdg'

# 获取所有bdg文件
files = [f for f in os.listdir(folder_path) if f.endswith('aligned.bdg')]

# 初始化一个空列表来存储所有样本的数据
data = []
sample_names = []  # 用于存储样本文件名

# 遍历每个文件，提取第4列数据
for file in files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path, sep='\t', header=None)
    # 确保文件有足够的列
    if df.shape[1] >= 4:
        # 提取第4列并将其转化为numpy数组
        data.append(df.iloc[:, 3].values)
        # 记录样本文件名
        sample_names.append(file)
    else:
        print(f"Warning: {file} does not have enough columns.")

# 将所有样本的数据合并成一个数据矩阵，**不要进行转置**
data_matrix = np.array(data)

# %%
# 检查数据矩阵和样本名是否匹配
print(f"Data Matrix Shape: {data_matrix.shape}, Number of Samples: {len(sample_names)}")
# Output: Data Matrix Shape: (17855, 2781), Number of Samples: 17855

import numpy as np

# 计算每个样本（行）的和
sample_sums = np.sum(data_matrix, axis=1)

# %%
# 标准化数据
scaler = StandardScaler()
data_matrix_scaled = scaler.fit_transform(data_matrix)

# %%
# PCA降维
pca = PCA(n_components=50)  # 可以根据需要调整主成分的数量
pca_result = pca.fit_transform(data_matrix_scaled)


# %%
# UMAP降维
umap_model = umap.UMAP(n_neighbors=15, min_dist=0.1, n_components=2, random_state=42)
umap_result = umap_model.fit_transform(pca_result)

# KMeans聚类
kmeans = KMeans(n_clusters=4, random_state=42)  # 可以根据需要调整簇的数量
clusters = kmeans.fit_predict(umap_result)


# 确保 clusters 为字符串类型并按顺序设置类别
clusters = pd.Categorical(clusters, categories=sorted(set(clusters)), ordered=True)

# 重新创建图像
plt.figure(figsize=(10, 8))

# 使用对比度更高的调色板，例如 'Set2'
scatter = sns.scatterplot(
    x=umap_result[:, 0],
    y=umap_result[:, 1],
    hue=clusters.astype(str),
    palette='Set2',  # 更高对比度的调色板
    s=50,
    alpha=0.7
)
plt.title('UMAP Projection with KMeans Clustering')
plt.xlabel('UMAP1')
plt.ylabel('UMAP2')

# 获取图例句柄和标签，并确保图例按照定义的顺序显示
handles, labels = scatter.get_legend_handles_labels()
sorted_handles_labels = sorted(zip(handles, labels), key=lambda x: int(x[1]))  # 根据标签排序
handles, labels = zip(*sorted_handles_labels)
plt.legend(
    handles=handles,
    labels=labels,
    title='Cluster',
    bbox_to_anchor=(1.05, 1),
    loc='upper left'
)

# 保存图像
plt.savefig('/cluster/facility/yzhang/SHX/code/scCut-Tag/all-n500-k8.pdf', format='pdf', bbox_inches='tight')

# 显示图像
plt.show()
