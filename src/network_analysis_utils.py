import networkx as nx
import matplotlib.pyplot as plt

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
    >>> network_data = nx.DiGraph()
    >>> network_data.add_edge(1, 2, weight=0.5)
    >>> network_data.add_edge(1, 3, weight=9.8)
    >>> network_data.add_edge(2, 3, weight=0.5)
    >>> network_data.add_edge(3, 1, weight=0.5)
    >>> network_stats = calculate_network_summary_statistics(network_data)
    Calculating network summary statistics...
    Number of nodes:  3
    Number of edges:  4
    Calculating clustering coefficient...
    Clustering coefficient:  0.3333333333333333
    Calculating modularity...
    Modularity:  0.0
    Calculating connected components...
    Number of connected components:  1
    Calculating edge density...
    Edge density:  0.6666666666666666
    Calculating diameter...
    Diameter:  2
    Calculating average shortest path length...
    Average shortest path length:  1.3333333333333333
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
    print("Calculating modularity...")
    network_stats['modularity'] = nx.algorithms.community.modularity(network_data, nx.algorithms.community.label_propagation_communities(network_data))
    print("Modularity: ", network_stats['modularity'])
    print("Calculating connected components...")
    network_stats['connected_components'] = nx.number_connected_components(network_data)
    print("Number of connected components: ", network_stats['connected_components'])
    print("Calculating edge density...")
    network_stats['edge_density'] = nx.density(network_data)
    print("Edge density: ", network_stats['edge_density'])
    print("Calculating diameter...")
    network_stats['diameter'] = nx.diameter(network_data)
    print("Diameter: ", network_stats['diameter'])
    print("Calculating average shortest path length...")
    network_stats['average_shortest_path_length'] = nx.average_shortest_path_length(network_data)
    print("Average shortest path length: ", network_stats['average_shortest_path_length'])
    print("Calculating degree distribution...")
    degrees = [network_data.degree(n) for n in network_data.nodes()]
    plt.hist(degrees)
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
    >>> negative_nodes = np.array([2, 1])
    >>> centralities = calculate_centralities_negative_nodes(network_data, negative_nodes)
    >>> centralities['degree_centrality']
    {1: 0.3333333333333333, 2: 0.3333333333333333}
    >>> centralities['betweenness_centrality']
    {1: 0.0, 2: 0.0}
    >>> centralities['eigenvector_centrality']
    {1: 0.5773502691896256, 2: 0.5773502691896256}
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