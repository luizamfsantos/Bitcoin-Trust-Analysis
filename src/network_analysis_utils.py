import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def calculate_network_summary_statistics(network_data):
    '''
    Calculate basic network summary statistics

    Parameters
    ----------
    network_data: Weighted DiGraph
        The network to be analyzed
    
    Returns
    -------
    network_stats: dict
        A dictionary containing the statistics on the network
            number_of_nodes: number of nodes in the network
            number_of_edges: number of edges in the network
            clustering_coefficient: clustering coefficient of the network
            modularity: modularity of the network
            connected_components: number of connected components in the network
            edge_density: edge density of the network
            diameter: diameter of the network
            average_shortest_path_length: average shortest path length of the network

            
    Prints
    ------
    Graph:
        Shows the distribution of the degrees of the nodes in the network
    Additional information:
        Prints the values of the network summary statistics

    Examples
    --------
    >>> import networkx as nx
    >>> import matplotlib.pyplot as plt
    >>> network_data = nx.Graph()
    >>> network_data.add_edge(1, 2, weight=0.5)
    >>> network_data.add_edge(1, 3, weight=9.8)
    >>> network_data.add_edge(2, 3, weight=0.5)
    >>> network_data.add_edge(3, 1, weight=0.5)
    >>> network_stats = calculate_network_summary_statistics(network_data)
    Calculating network summary statistics...
    Number of nodes:  3
    Number of edges:  3
    Calculating clustering coefficient...
    Clustering coefficient:  1.0
    Calculating modularity...
    Modularity:  0.0
    Calculating connected components...
    Number of connected components:  1
    Calculating edge density...
    Edge density:  1.0
    Calculating diameter...
    Diameter:  1
    Calculating average shortest path length...
    Average shortest path length:  1.0
    Calculating degree distribution...
    '''
    network_stats = {}
    print("Calculating network summary statistics...")
    network_stats['number_of_nodes'] = network_data.number_of_nodes()
    print("Number of nodes: ", network_stats['number_of_nodes'])
    network_stats['number_of_edges'] = network_data.number_of_edges()
    print("Number of edges: ", network_stats['number_of_edges'])
    print("Calculating clustering coefficient...")
    network_stats['clustering_coefficient'] = nx.average_clustering(network_data)
    print("Clustering coefficient: ", network_stats['clustering_coefficient'])
    # check if the network is undirected
    if nx.is_directed(network_data) is False:
        print("Calculating modularity...")
        network_stats['modularity'] = nx.algorithms.community.modularity(network_data, nx.algorithms.community.label_propagation_communities(network_data))
        print("Modularity: ", network_stats['modularity'])
        print("Calculating connected components...")
        network_stats['connected_components'] = nx.number_connected_components(network_data)
        print("Number of connected components: ", network_stats['connected_components'])
    else:
        network_stats['modularity'] = None
        network_stats['connected_components'] = None
    print("Calculating edge density...")
    network_stats['edge_density'] = nx.density(network_data)
    print("Edge density: ", network_stats['edge_density'])
    print("Calculating diameter...")
    try:
        network_stats['diameter'] = nx.diameter(network_data)
    except nx.exception.NetworkXError:
        network_stats['diameter'] = None
    print("Diameter: ", network_stats['diameter'])
    print("Calculating average shortest path length...")
    if network_stats['diameter'] == None:
        network_stats['average_shortest_path_length'] = None
    else:
        network_stats['average_shortest_path_length'] = nx.average_shortest_path_length(network_data)
    print("Average shortest path length: ", network_stats['average_shortest_path_length'])
    print("Calculating degree distribution...")
    degrees = [network_data.degree(n) for n in network_data.nodes()]
    bins = list(range(0, 101, 10))  # defining bins from 0 to 100 with step 10
    plt.hist(degrees, bins=bins)
    plt.xticks(bins)  # setting x-axis ticks to the bin edges
    plt.xlabel('Degree')
    plt.ylabel('Frequency')
    plt.title('Degree Distribution')
    plt.show()
    return network_stats


def create_negative_nodes_subgraph(graph, negative_node_list):
    '''
    Create a subgraph of negative nodes
    
    Parameters
    ----------
    graph: Weighted DiGraph
        The network to be analyzed
    negative_node_list: numpy array
        The nodes that have negative TRUST_INDEX values
        
    Returns
    -------
    negative_nodes_graph: Weighted DiGraph
        The subgraph of negative nodes
    
    Examples
    --------
    >>> import networkx as nx
    >>> import matplotlib.pyplot as plt
    >>> network_data = nx.DiGraph()
    >>> network_data.add_edge(1, 2, weight=0.5)
    >>> network_data.add_edge(1, 3, weight=-9.8)
    >>> network_data.add_edge(2, 3, weight=-0.5)
    >>> network_data.add_edge(3, 1, weight=0.5)
    >>> negative_nodes = np.array([2, 1])
    >>> negative_nodes_graph = create_negative_nodes_subgraph(network_data, negative_nodes)
    >>> negative_nodes_graph.edges(data=True)
    OutEdgeDataView([(1, 3, {'weight': -9.8}), (2, 3, {'weight': -0.5})])
    '''
    # Create a subgraph of negative nodes, include only edges that have a node from negative_node_list in either TO_NODE or FROM_NODE
    negative_nodes_graph = nx.DiGraph()
    for node in negative_node_list:
        negative_nodes_graph.add_node(node)
    for edge in graph.edges():
        if edge[0] in negative_node_list or edge[1] in negative_node_list:
            negative_nodes_graph.add_edge(edge[0], edge[1])



def visualize_network_of_negative_nodes(negative_nodes_graph, negative_node_list):
    '''
    Visualize communities of negative nodes in the network

    Parameters
    ----------
    negative_nodes_graph: Weighted DiGraph
        The network to be analyzed
    negative_node_list: numpy array

    Returns
    -------
    None

    Prints
    ------
    Graph:
        Shows the communities of negative nodes in the network
        Color negative_node_list nodes red and the rest of the nodes blue
    
    Examples
    --------
    >>> import networkx as nx
    >>> import matplotlib.pyplot as plt
    >>> data = pd.DataFrame({'FROM_NODE': np.array([1, 2, 3, 4]), 'TO_NODE': np.array([2, 3, 4, 1]), 'TRUST_INDEX': np.array([1, -1, 1, -1])})
    >>> network_data = create_direct_network(data)
    >>> negative_nodes = select_negative_nodes(data)
    >>> visualize_network_of_negative_nodes(network_data, negative_nodes)
    '''
    # Create list of nodes that are in negative_node_list and in negative_nodes_graph
    negative_node_list = [node for node in negative_node_list if node in negative_nodes_graph.nodes]
    # Visualize the subgraph
    pos = nx.spring_layout(negative_nodes_graph)
    nx.draw_networkx_nodes(negative_nodes_graph, pos, cmap=plt.get_cmap('jet'), node_size=500)
    nx.draw_networkx_edges(negative_nodes_graph, pos, edgelist=negative_nodes_graph.edges(), edge_color='black')
    nx.draw_networkx_nodes(negative_nodes_graph, pos, nodelist=negative_node_list, node_color='r', node_size=500)
    plt.show()

def calculate_centralities_negative_nodes(graph, negative_nodes_list):
    '''
    Calculate centrality measures for each node in negative_nodes_list
        Include calculate degree centrality, betweenness centrality, eigenvector centrality
    
    Parameters
    ----------
    graph: Weighted DiGraph
        The network to be analyzed
    negative_nodes_list: numpy array
        The nodes that have negative TRUST_INDEX values
    
    Returns
    -------
    centralities: dict
        A dictionary containing the centrality measures for each node in negative_nodes_list
            degree_centrality: degree centrality of each node in negative_nodes_list
            betweenness_centrality: betweenness centrality of each node in negative_nodes_list
            eigenvector_centrality: eigenvector centrality of each node in negative_nodes_list
    
    Examples
    --------
    >>> import networkx as nx
    >>> import matplotlib.pyplot as plt
    >>> network_data = nx.DiGraph()
    >>> network_data.add_edge(1, 2, weight=0.5)
    >>> network_data.add_edge(1, 3, weight=-9.8)
    >>> network_data.add_edge(2, 3, weight=-0.5)
    >>> network_data.add_edge(3, 1, weight=0.5)
    >>> negative_nodes = np.array([1, 2])
    >>> centralities = calculate_centralities_negative_nodes(network_data, negative_nodes)
    >>> centralities['degree_centrality']
    {1: 1.5, 2: 1.0}
    >>> centralities['betweenness_centrality']
    {1: 0.5, 2: 0.0}
    >>> centralities['eigenvector_centrality']
    {1: 0.5484320099232192, 2: 0.4139987636359533}
    '''
    centralities = {}
    centralities['degree_centrality'] = nx.degree_centrality(graph)
    centralities['betweenness_centrality'] = nx.betweenness_centrality(graph)
    centralities['eigenvector_centrality'] = nx.eigenvector_centrality(graph)
    # filter the centralities to only include the nodes in negative_nodes_list
    negative_nodes_centralities = {}
    for key in centralities.keys():
        negative_nodes_centralities[key] = {k: centralities[key][k] for k in negative_nodes_list}
    return negative_nodes_centralities

def calculate_mean_centrality_negative_nodes(negative_nodes_centralities):
    '''
    Calculate the mean centrality for each centrality measure in negative_nodes_centralities

    Parameters
    ----------
    negative_nodes_centralities: dict
        A dictionary containing the centrality measures for each node in negative_nodes_list
            degree_centrality: degree centrality of each node in negative_nodes_list
            betweenness_centrality: betweenness centrality of each node in negative_nodes_list
            eigenvector_centrality: eigenvector centrality of each node in negative_nodes_list
    
    Returns
    -------
    mean_centrality: dict
        A dictionary containing the mean centrality for each centrality measure in negative_nodes_centralities
    
    Examples
    --------
    >>> import networkx as nx
    >>> import matplotlib.pyplot as plt
    >>> network_data = nx.DiGraph()
    >>> network_data.add_edge(1, 2, weight=0.5)
    >>> network_data.add_edge(1, 3, weight=-9.8)
    >>> network_data.add_edge(2, 3, weight=-0.5)
    >>> network_data.add_edge(3, 1, weight=0.5)
    >>> negative_nodes = np.array([2, 1])
    >>> centralities = calculate_centralities_negative_nodes(network_data, negative_nodes)
    >>> mean_centrality = calculate_mean_centrality_negative_nodes(centralities)
    >>> mean_centrality['degree_centrality']
    1.25
    >>> mean_centrality['betweenness_centrality']
    0.25
    >>> mean_centrality['eigenvector_centrality']
    0.4812153867795862
    '''
    mean_centrality = {}
    for key in negative_nodes_centralities.keys():
        mean_centrality[key] = np.mean(list(negative_nodes_centralities[key].values()))
    return mean_centrality

def time_series_centralities(*centrality_dicts):
    '''
    Create 3 subplots to represent the centrality measures calculated from calculate_mean_centrality_negative_nodes and plot them over time
        Make sure each graph is in order starting with period 0 until period n
    
    Parameters
    ----------
    *centrality_dicts: dict
        A dictionary containing the centrality measures for each node in negative_nodes_list
            degree_centrality: degree centrality of each node in negative_nodes_list
            betweenness_centrality: betweenness centrality of each node in negative_nodes_list
            eigenvector_centrality: eigenvector centrality of each node in negative_nodes_list
            
    Returns
    -------
    None

    Prints
    ------
    Graph:
        Shows the time series of the centrality measures for each period
    
    Examples
    --------
    >>> import networkx as nx
    >>> import matplotlib.pyplot as plt
    >>> network_data_period_0 = nx.DiGraph()
    >>> network_data_period_0.add_edge(1, 2, weight=0.5)
    >>> network_data_period_0.add_edge(1, 3, weight=-9.8)
    >>> network_data_period_0.add_edge(2, 3, weight=-0.5)
    >>> network_data_period_0.add_edge(3, 1, weight=0.5)
    >>> negative_nodes_period_0 = np.array([2, 1])
    >>> centralities_period_0 = calculate_centralities_negative_nodes(network_data_period_0, negative_nodes_period_0)
    >>> mean_centrality_period_0 = calculate_mean_centrality_negative_nodes(centralities_period_0)
    >>> network_data_period_1 = nx.DiGraph()
    >>> network_data_period_1.add_edge(1, 2, weight=0.5)
    >>> network_data_period_1.add_edge(1, 3, weight=-9.8)
    >>> network_data_period_1.add_edge(2, 3, weight=-0.5)
    >>> network_data_period_1.add_edge(3, 1, weight=0.5)
    >>> negative_nodes_period_1 = np.array([2, 1])
    >>> centralities_period_1 = calculate_centralities_negative_nodes(network_data_period_1, negative_nodes_period_1)
    >>> mean_centrality_period_1 = calculate_mean_centrality_negative_nodes(centralities_period_1)
    >>> time_series_centralities(mean_centrality_period_0, mean_centrality_period_1)
    '''
    num_periods = len(centrality_dicts)
    # Create a figure with 3 subplots
    fig, axs = plt.subplots(3)
    # Plot the degree centrality time series
    for i in range(num_periods):
        axs[0].plot(list(centrality_dicts[i]['degree_centrality'].values()), label='Period ' + str(i))
    axs[0].set_title('Degree Centrality')
    axs[0].legend()
    # Plot the betweenness centrality time series
    for i in range(num_periods):
        axs[1].plot(list(centrality_dicts[i]['betweenness_centrality'].values()), label='Period ' + str(i))
    axs[1].set_title('Betweenness Centrality')
    axs[1].legend()
    # Plot the eigenvector centrality time series
    for i in range(num_periods):
        axs[2].plot(list(centrality_dicts[i]['eigenvector_centrality'].values()), label='Period ' + str(i))
    axs[2].set_title('Eigenvector Centrality')
    axs[2].legend()
    # Show the figure
    plt.show()

if __name__ == "__main__":
    from data_preprocessing import create_direct_network, select_negative_nodes
    import doctest
    doctest.testmod()