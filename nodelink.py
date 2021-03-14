import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import sys
from sys import argv
import os

URL_DATASET = r"/home/kunika/Desktop/Data_viz/Datathon_3/COVID19/archive/"



Data_path = URL_DATASET + "time_series_covid_19_" + sys.argv[1] + "_US.csv"
cases  = pd.read_csv(Data_path)

cases =  cases.groupby('Province_State').sum()

cases =  cases[1:].transpose()

cases = cases.drop([cases.index[0], cases.index[2], cases.index[3]])



# print(cases.to_string())


cor_matrix = cases.iloc[:,1:].corr() #craetes a correlation matrix

# print(cor_matrix.head())

deaths = cor_matrix.index.values


cor_matrix = np.asmatrix(cor_matrix) #Changes from dataframe to matrix, so it is easier to create a graph with networkx


G = nx.from_numpy_matrix(cor_matrix)


G = nx.relabel_nodes(G,lambda x: deaths[x]) #relabels the nodes to match the  stocks names


G.edges(data=True) #shows the edges with their corresponding weights




def create_corr_network(G, corr_direction, min_correlation):

    ##Creates a copy of the graph
    H = G.copy()

    if corr_direction == "positive":
    	edge_colour = plt.cm.YlOrRd
    else:
    	edge_colour = plt.cm.Greys

    ##Checks all the edges and removes some based on corr_direction
    for case1, case2, weight in list(G.edges(data=True)):
        ##if we only want to see the positive correlations we then delete the edges with weight smaller than 0
        if corr_direction == "positive":
            if weight["weight"] <0 or weight["weight"] < min_correlation:
                H.remove_edge(case1, case2)
        ##this part runs if the corr_direction is negative and removes edges with weights equal or largen than 0
        else:
            if weight["weight"] >=0 or weight["weight"] > min_correlation:
                H.remove_edge(case1, case2)

    edges,weights = zip(*nx.get_edge_attributes(H,'weight').items())

    #positions

    pos = lambda x : nx.spring_layout(H, k = 0.7) if argv[2] == "spring" else (nx.random_layout(H) if argv[2] == "random" else (nx.circular_layout(H, scale = 1) if argv[2] == "circular" else (nx.fruchterman_reingold_layout(H, k = 0.7))))
    positions = pos(argv[2])
    # positions = nx.fruchterman_reingold_layout(H)
    
    #Figure size
    plt.figure(figsize=(15,15))

    #draws nodes
    nx.draw_networkx_nodes(H,positions,node_color='#05d7fc',
                           node_size=500,alpha=0.6)
    
    #Styling for labels
    nx.draw_networkx_labels(H, positions, font_size=8, 
                            font_family='sans-serif')
        
    #draws the edges
    # nx.draw_networkx_edges(G, positions, edgelist=edges,style='solid')
    
    nx.draw_networkx_edges(H, positions, edgelist=edges,style='solid', width=weights, edge_color = weights, edge_cmap = edge_colour,
                      edge_vmin = min(weights), edge_vmax=max(weights))
    d = nx.degree(H)
    # print(d)
    # degree_values = [v for k, v in d]

    # print(degree_values)
    nodelist, node_sizes = zip(*d)
    nx.draw_networkx_nodes(G,positions,node_color='#05d7fc',nodelist=nodelist,
                       #####the node size will be now based on its degree
                       node_size=tuple([x**0.3 for x in node_sizes]),alpha=0.8)
    
    # displays the graph without axis
    plt.axis('off')
    #saves image
    if os.path.exists(URL_DATASET + '/Results/US/nodelink/' + sys.argv[1]):
    	pass
    else:
    	os.makedirs(URL_DATASET + '/Results/US/nodelink/' + sys.argv[1])

    results_dir = URL_DATASET + '/Results/US/nodelink/' + sys.argv[1] + "/" 

    fname = sys.argv[2] + "_" + argv[3] + ".png"
    plt.savefig(os.path.join(results_dir, fname), format="PNG")
    # plt.show() 




create_corr_network(G, corr_direction=argv[3], min_correlation= float(argv[4]))
