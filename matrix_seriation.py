import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from sys import argv
import os
from scipy.spatial.distance import pdist, squareform
from sklearn import datasets
from fastcluster import linkage

URL_DATASET = r"/home/kunika/Desktop/Data_viz/Datathon_3/COVID19/archive/"



Data_path = URL_DATASET + "time_series_covid_19_" + sys.argv[1] + "_US.csv"
cases  = pd.read_csv(Data_path)
list_countries = cases['Province_State'].unique().tolist()
# print(list_countries)



cases =  cases.groupby('Province_State').sum()

cases =  cases[1:].transpose()

cases = cases.drop([cases.index[0]])

# print(cases.index[1])
# print(cases.to_string())


cor_matrix = cases.iloc[:,1:].corr() #craetes a correlation matrix

# print(cases.iloc[:,1:])

# print(cor_matrix.head().to_string())

# deaths = cor_matrix.index.values
# dist_mat = squareform(pdist(cases.iloc[:,1:]))
N = len(cor_matrix)
dist_mat = np.asmatrix(cor_matrix) #Changes from dataframe to matrix, so it is easier to create a graph with networkx
# print(dist_mat)

# X = cases[np.random.permutation(N),:]
fig, ax = plt.subplots()
fig.set_size_inches(12, 10)
plt.pcolormesh(cor_matrix)
# clb = plt.colorbar()
# plt.colorbar.label()
m = plt.cm.ScalarMappable(cmap= plt.cm.viridis)
# m.set_array(z)
m.set_clim(0, 1)
cbar = plt.colorbar(m)
# cbar = plt.colorbar()
cbar.set_label(sys.argv[1], rotation=0, labelpad=-20, y=1.05, fontsize = 10)
# clb.ax.set_title()
plt.xlim([0,N])
plt.ylim([0,N])
plt.title(" correlation matrix for COVID19 dataset of " + sys.argv[2] + " " + sys.argv[1] + " cases", fontsize=8)
if os.path.exists(URL_DATASET + '/Results/Matrix_Seriation/' + sys.argv[2] + '/' + sys.argv[1] + '/' + sys.argv[3] ):
   	pass
else:
    os.makedirs(URL_DATASET + '/Results/Matrix_Seriation/' + sys.argv[2] + '/' + sys.argv[1] + '/' + sys.argv[3])

results_dir = URL_DATASET + '/Results/Matrix_Seriation/' + sys.argv[2] + '/' + sys.argv[1] + '/' + sys.argv[3] + "/" 
fname = "dist_mat.png"
labels = list_countries[:-1]
x = np.array(range(N+1))
plt.xticks(x, labels, rotation ='vertical', fontsize = 4)
plt.yticks(x, labels, rotation ='horizontal', fontsize = 4) 
plt.savefig(os.path.join(results_dir, fname), format="PNG")


def seriation(Z,N,cur_index):
    '''
        input:
            - Z is a hierarchical tree (dendrogram)
            - N is the number of points given to the clustering process
            - cur_index is the position in the tree for the recursive traversal
        output:
            - order implied by the hierarchical tree Z
            
        seriation computes the order implied by a hierarchical tree (dendrogram)
    '''
    if cur_index < N:
        return [cur_index]
    else:
        left = int(Z[cur_index-N,0])
        right = int(Z[cur_index-N,1])
        return (seriation(Z,N,left) + seriation(Z,N,right))
    
def compute_serial_matrix(dist_mat,method):
    '''
        input:
            - dist_mat is a distance matrix
            - method = ["ward","single","average","complete"]
        output:
            - seriated_dist is the input dist_mat,
              but with re-ordered rows and columns
              according to the seriation, i.e. the
              order implied by the hierarchical tree
            - res_order is the order implied by
              the hierarhical tree
            - res_linkage is the hierarhical tree (dendrogram)
        
        compute_serial_matrix transforms a distance matrix into 
        a sorted distance matrix according to the order implied 
        by the hierarchical tree (dendrogram)
    '''
    N = len(dist_mat)
    flat_dist_mat = dist_mat
    res_linkage = linkage(flat_dist_mat, method=method,preserve_input=True)
    res_order = seriation(res_linkage, N, N + N-2)
    seriated_dist = np.zeros((N,N))
    a,b = np.triu_indices(N,k=1)
    seriated_dist[a,b] = dist_mat[ [res_order[i] for i in a], [res_order[j] for j in b]]
    seriated_dist[b,a] = seriated_dist[a,b]
    
    return seriated_dist, res_order, res_linkage


# methods = ["ward","single","average","complete"]
# for method in methods:
    # print("Method:\t",method)
method = sys.argv[3] 
ordered_dist_mat, res_order, res_linkage = compute_serial_matrix(dist_mat,method)

# print(res_linkage)

# print(ordered_dist_mat)
# ax = sns.heatmap(
#     ordered_dist_mat, 
#     vmin=-1, vmax=1, center=0,
#     cmap=sns.diverging_palette(20, 220, n=200),
#     square=True
# )
# ax.set_xticklabels(
#     ax.get_xticklabels(),
#     rotation=45,
#     horizontalalignment='right'
# );
fig, ax = plt.subplots()
fig.set_size_inches(12, 10)
m = plt.cm.ScalarMappable(cmap= plt.cm.viridis)
# m.set_array(z)
m.set_clim(0, 1)
cbar = plt.colorbar(m)
# cbar = plt.colorbar()
cbar.set_label(sys.argv[1], rotation=0, labelpad=-20, y=1.05, fontsize = 10)

plt.pcolormesh(ordered_dist_mat)
plt.xlim([0,N])
plt.ylim([0,N])
x = np.array(range(N))
# my_xticks = np.array(range())
# plt.xticks(x, list_countries)

# plt.ylabel("", fontsize=12)
if os.path.exists(URL_DATASET + '/Results/Matrix_Seriation/' + sys.argv[2] + '/' + sys.argv[1] + '/' + sys.argv[3] ):
   	pass
else:
    os.makedirs(URL_DATASET + '/Results/Matrix_Seriation/' + sys.argv[2] + '/' + sys.argv[1] + '/' + sys.argv[3])

results_dir = URL_DATASET + '/Results/Matrix_Seriation/' + sys.argv[2] + '/' + sys.argv[1] + '/' + sys.argv[3] + "/" 
labels = res_order
fname = "ordered_dist_mat.png"
plt.title(sys.argv[3] + " seriated matrix for COVID19 dataset of " + sys.argv[2] + " " + sys.argv[1] + " cases", fontsize=10)
plt.xticks(x, labels, rotation ='vertical', fontsize = 4)
plt.yticks(x, labels, rotation ='horizontal', fontsize = 4) 
plt.savefig(os.path.join(results_dir, fname), format="PNG")

# plt.xlabel()
    # plt.show() 

    # plt.show()

