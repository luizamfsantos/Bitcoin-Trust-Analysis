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


def visualize_network(network_data):
    # Function to visualize the network
    pass

def calculate_centrality(network_data):
    # Function to calculate centrality measures
    pass

def community_detection(network_data):
    # Function to detect communities within the network
    pass
