import pandas as pd
import numpy as np

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
