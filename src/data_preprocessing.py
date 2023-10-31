import pandas as pd
import numpy as np
import sys, os
from datetime import datetime
import networkx as nx

def signed_data(data):
    '''
    Function to modify the data to keep only the sign of the trust values
    
    Parameters
    ----------
    data: pandas DataFrame
        The data to be modified
        It should have a column called TRUST_INDEX
    
    Returns
    -------
    data_signed: pandas DataFrame
        The modified data
    
    Examples
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> data = pd.DataFrame({'TRUST_INDEX': np.array([5, -3, 2, -8])})
    >>> data_signed = signed_data(data)
    >>> data_signed
       TRUST_INDEX
    0          1.0
    1         -1.0
    2          1.0
    3         -1.0
    '''
    data_signed = data.copy()
    data_signed['TRUST_INDEX'] = np.sign(data_signed['TRUST_INDEX'])
    return data_signed

def epoch_to_datetime(data):
    '''
    Change the epoch time to datetime

    Parameters
    ----------
    data: pandas DataFrame
        The data to be modified
        It should have a column called TIME_SINCE_EPOCH

    Returns
    -------
    data: pandas DataFrame
        The modified data
        Instead of the column TIME_SINCE_EPOCH,
            there is a column called TIME

    Examples
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> from datetime import datetime
    >>> data = pd.DataFrame({'TIME_SINCE_EPOCH': np.array([1546300800, 1546387200, 1546473600, 1546560000])})
    >>> data_timed = epoch_to_datetime(data)
    >>> data_timed
                    TIME
    0 2019-01-01 00:00:00
    1 2019-01-02 00:00:00
    2 2019-01-03 00:00:00
    3 2019-01-04 00:00:00
    '''
    data['TIME'] = data['TIME_SINCE_EPOCH'].apply(lambda x: datetime.fromtimestamp(x))
    data = data.drop('TIME_SINCE_EPOCH', axis=1)
    return data

def divide_data_into_periods(data,num_periods):
    '''
    Divides the input DataFrame into num_periods equally spaced periods based on time intervals.

    Parameters
    ----------
    data: pandas DataFrame
        The data to be modified
        It should have a column called TIME
    num_periods: int
        The number of periods to divide the data into
    
    Returns
    -------
    data: pandas DataFrame
        The modified data
        Instead of the column TIME,
            there is a column called PERIOD
    
    Examples
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> from datetime import datetime
    >>> data = pd.DataFrame({'TIME': np.array([datetime(2019,1,1), datetime(2019,1,2), datetime(2019,1,3), datetime(2019,1,4)])})
    >>> data_timed = divide_data_into_periods(data,2)
    >>> data_timed
       PERIOD
    0       0
    1       0
    2       1
    3       1
    '''
    data['PERIOD'] = pd.cut(data['TIME'], bins=num_periods, labels=False)
    data = data.drop('TIME', axis=1)
    return data

def select_negative_nodes(data):
    '''
    This function selects the TO_NODEs that have negative TRUST_INDEX values

    Parameters
    ----------
    data: pandas DataFrame
        The data to be modified
        It should have columns FROM_NODE,TO_NODE and TRUST_INDEX
    
    Returns
    -------
    negative_nodes: numpy array
        The nodes that have negative TRUST_INDEX values
    
    Examples
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> data = pd.DataFrame({'FROM_NODE': np.array([1, 2, 3, 4]), 'TO_NODE': np.array([2, 3, 4, 1]), 'TRUST_INDEX': np.array([1, -1, 1, -1])})
    >>> negative_nodes = select_negative_nodes(data)
    >>> negative_nodes
    array([2, 1])
    '''
    data_negative = data[data['TRUST_INDEX'] < 0]
    negative_nodes = data_negative['TO_NODE'].unique()
    return negative_nodes

def create_direct_network(data):
    '''
    Create weighted DiGraph from data

    Parameter
    ---------
    data: pandas DataFrame
        It should contain the columns FROM_NODE,TO_NODE and TRUST_INDEX
        The TRUST_INDEX will correspond to the weight of each node
    
    Returns
    -------
    network_data: Weighted DiGraph
        The network created from data
    
    Examples
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> data = pd.DataFrame({'FROM_NODE': np.array([1, 2, 3, 4]), 'TO_NODE': np.array([2, 3, 4, 1]), 'TRUST_INDEX': np.array([1, -1, 1, -1])})
    >>> network_data = create_direct_network(data)
    >>> network_data.edges(data=True)
    OutEdgeDataView([(1, 2, {'weight': 1}), (2, 3, {'weight': -1}), (3, 4, {'weight': 1}), (4, 1, {'weight': -1})])
    '''
    network_data = nx.from_pandas_edgelist(data, 'FROM_NODE', 'TO_NODE', edge_attr='TRUST_INDEX', create_using=nx.DiGraph())
    return network_data



if __name__ == '__main__':
    # append the path of the project directory to the system path
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    file_path = "data/processed/soc-sign-bitcoinotc-signed.csv"
    lines = 100
    data = pd.read_csv(file_path, nrows=lines,header=0)
    print(data.head())
    data_timed = epoch_to_datetime(data)
    print(data_timed.head())
    