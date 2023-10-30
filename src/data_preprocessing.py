import pandas as pd
import numpy as np
import sys, os
from datetime import datetime

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

def clean_data(data):
    # Function to clean the raw data
    pass

def transform_data(data):
    # Function to transform data for analysis
    pass

def prepare_data(data):
    # Function to prepare data for modeling
    pass


if __name__ == '__main__':
    # append the path of the project directory to the system path
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    file_path = "data/processed/soc-sign-bitcoinotc-signed.csv"
    lines = 100
    data = pd.read_csv(file_path, nrows=lines,header=0)
    print(data.head())
    data_timed = epoch_to_datetime(data)
    print(data_timed.head())
    