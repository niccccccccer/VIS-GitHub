from sentence_transformers import SentenceTransformer
import json
import time
import numpy as np
owner="modelmapper"
repo="modelmapper"
data=[]

with open(f'../assets/data/{owner}_{repo}_pulls.json', "r") as f:
    data = json.load(f)
model = SentenceTransformer('all-MiniLM-L6-v2')
start_time = time.time()

# query='how to skip conflict'
# query="implict mapping and explict mapping"
query="go"
# query_embedding = model.encode(query)
# query_embedding = np.array(query_embedding)
# query_embedding = query_embedding.reshape(query_embedding.shape[0],1)
# query_embeddings=np.array([query_embedding])

sentences = []
for item in data:
    sentences.append(item['title']+item['body'])
sentences.append(query)

#Sentences are encoded by calling model.encode()
embeddings = model.encode(sentences)


end_time = time.time()
print("The number of pr is %d.\nTotal time taken in seconds:%f" %(len(data),end_time - start_time))
# print(embeddings[0].shape)  # length 384

#Print the embeddings
# for sentence, embedding in zip(sentences, embeddings):
#     print("Sentence:", sentence)
#     print("Embedding:", embedding)
#     print("")


from sklearn.manifold import TSNE
from sklearn.datasets import load_iris,load_digits
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
#---------------TSNE-------------------
def prepocessing_tsne(data, n,i):
    
    starttime_tsne = time.time()
    dataset = TSNE(n_components=n, random_state=33).fit_transform(data)
    endtime_tsne = time.time()
    print('%dcost time by tsne: %f' %(i, endtime_tsne-starttime_tsne))
    scaler = MinMaxScaler(feature_range=(0, 1))
    X_tsne = scaler.fit_transform(dataset)
    return X_tsne
#---------------PCA-------------------
def prepocessing_pca(data, n,i):
    
    starttime_pca = time.time()
    dataset = PCA(n_components=n).fit_transform(data)
    endtime_pca = time.time()
    print('%dcost time by pca: %f'%(i,endtime_pca-starttime_pca))
    scaler = MinMaxScaler(feature_range=(0, 1))
    X_pca = scaler.fit_transform(dataset) 
    return X_pca
digits_tsne = []
digits_pca = []
for i in range(1,11):

    # start_time = time.time()
    digits_tsne = prepocessing_tsne(embeddings, 2,i)
    # end_time = time.time()
    # print("modelmapper for t-SNE: %f" %(end_time - start_time))

    # start_time = time.time()
    digits_pca = prepocessing_pca(embeddings, 2,i)
    # end_time = time.time()
# print("modelmapper for PCA: %f" %(end_time - start_time))
# query_tsne = prepocessing_tsne(query_embeddings, 2)
# query_pca = prepocessing_pca(query_embeddings, 2)
number=[]
title=[]
body=[]
for item in data:
    number.append(item['number'])
    title.append(item['title'])
    body.append(item['body'])
print("number length",len(number))
number.append("null")
title.append(query)
body.append("null")
# x and y given as DataFrame columns
import plotly.express as px
digits_tsne = pd.DataFrame(digits_tsne, columns=['x', 'y'])
# query_tsne = pd.DataFrame(query_tsne, columns=['x', 'y'])
digits_tsne['number']=number
digits_tsne['title']=title
digits_tsne['body']=body
digits_tsne['color']='PR'
digits_tsne.loc[digits_tsne.shape[0]-1,'color']='query'

# query_tsne = pd.DataFrame(query_tsne, columns=['x', 'y'])
# query_tsne['color']=1
# digits_tsne = digits_tsne.append(query_tsne)

digits_pca= pd.DataFrame(digits_pca, columns=['x', 'y'])
print((digits_pca.shape[0]))
digits_pca['number']=number
digits_pca['title']=title
digits_pca['body']=body
digits_pca['color']='PR'
digits_pca.loc[digits_pca.shape[0]-1,'color']='query'

# query_pca = pd.DataFrame(query_pca, columns=['x', 'y'])
# query_pca['color']=1
# digits_pca = digits_pca.append(query_pca)

fig1 = px.scatter(digits_pca, x="x", y="y", color="color",hover_data=['number', 'title'])
fig1.layout.title = 'PCA'
fig1.show()
fig2 = px.scatter(digits_tsne, x="x", y="y", color="color",hover_data=['number', 'title'])
fig2.layout.title = 't-SNE'
fig2.show()

#--------plot--------

# sns.set_style("darkgrid") #设立风格

# plt.figure(figsize=(18, 8))

# plt.subplot(1, 2, 1) 
# plt.scatter(digits_tsne[:, 0], digits_tsne[:, 1], c=embeddings.target, alpha=0.6, 
#             cmap=plt.cm.get_cmap('rainbow', 10))
# plt.title("digits t-SNE", fontsize=18)
# cbar = plt.colorbar(ticks=range(10)) 
# cbar.set_label(label='digit value', fontsize=18)

# plt.subplot(1, 2, 2)
# plt.scatter(digits_pca[:, 0], digits_pca[:, 1], c=embeddings.target, alpha=0.6, 
#             cmap=plt.cm.get_cmap('rainbow', 10))
# plt.title("digits PCA", fontsize=18)
# cbar = plt.colorbar(ticks=range(10)) 
# cbar.set_label(label='digit value', fontsize=18)
# plt.tight_layout()
# plt.savefig('../assets/image/modelmapper.png', dpi=300)





# #---------------PCA-------------------
# import numpy as np
# import pandas as pd
# import seaborn as sns  #定义seaborn包
# import matplotlib.pyplot as plt  #定义matplotlib包
# from sklearn.decomposition import PCA   #导入PCA
# X_pca = PCA(n_components=2).fit_transform(embeddings)   
# # n_components为PCA的参数，所要保留的主成分个数n，也即保留下来的特征个数n
# # train_x_fea为需要降维的数据
# X_pca = np.vstack((X_pca.T, train_y)).T  #把降维后的数据和标签按垂直方向（行顺序）堆叠数组构成一个新的数组
# df_pca = pd.DataFrame(X_pca, columns=['1st_Component','2n_Component','label'])   #把降维后的数据和标签进行组合
# df_pca.head()
# plt.figure(figsize=(6, 6))  #定义输出图像大小
# sns.scatterplot(data=df_pca, hue='label',x='1st_Component',y='2n_Component')   #画散点图，定义X/Y轴
# plt.rcParams['xtick.direction'] = 'in'  #plt.rcParams主要作用是设置画的图的分辨率，大小等信息
# plt.rcParams['ytick.direction'] = 'in'
# plt.title('PCA visualization of features')  #定义标题
# plt.legend(loc='best')  #在最合适的地方显示便签
# plt.savefig('PCA visualization of features.jpg')  #保存图片
# plt.show()

# #---------------t-SNE-------------------
# from sklearn.manifold import TSNE 
# tsne = TSNE(n_components=2) 
# X_tsne = tsne.fit_transform(embeddings) 
# X_tsne_data = np.vstack((X_tsne.T, train_y)).T 
# df_tsne = pd.DataFrame(X_tsne_data, columns=['Dim1','Dim2','label']) 
# df_tsne.head()
# plt.figure(figsize=(6, 6)) 
# sns.scatterplot(data=df_tsne,hue='label',x='Dim1',y='Dim2')
# plt.title('T-SNE visualization of features')
# plt.legend(loc='best')
# plt.savefig('T-SNE visualization of features.jpg')
# plt.show()

# #---------------UMAP-------------------
# import umap
# import  seaborn as sns
# umap = umap.UMAP(n_components=2) 
# X_umap = umap.fit_transform(embeddings) 
# X_umap_data = np.vstack((X_umap.T, train_y)).T 
# df_umap = pd.DataFrame(X_umap_data, columns=['Dim1','Dim2','label']) 
# df_umap.head()
# plt.figure(figsize=(6, 6)) 
# sns.scatterplot(data=df_umap,hue='label',x='Dim1',y='Dim2')
# plt.title('Umap Visualization of features')
# plt.legend(loc='best')
# plt.savefig('Umap visualization of features.jpg')
# plt.show()


