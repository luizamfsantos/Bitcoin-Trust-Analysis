import pandas as pd
import numpy as np
import sys, os

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
    file_path = "data/raw/soc-sign-bitcoinotc.csv"
    # lines = 1000
    # data = pd.read_csv(file_path, nrows=lines,header=0)
    data = pd.read_csv(file_path, header=0)
    signed_data = signed_data(data)
    signed_data.to_csv("data/processed/soc-sign-bitcoinotc-signed.csv", index=False)