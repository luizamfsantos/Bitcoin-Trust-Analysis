import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data_preprocessing import epoch_to_datetime
import sys, os

def calculate_time_statistics(data):
    '''
    Calculate some statistics on time column

    Parameters
    ----------
    data: pandas DataFrame
        The data to be modified
        It should have a column called TIME
    
    Returns
    -------
    time_stats: dict
        A dictionary containing the statistics on the time column
            min: minimum value of the time column
            max: maximum value of the time column
            mean: mean value of the time column
            median: median value of the time column
            std: standard deviation of the time column
    
    Prints
    ------
    Graph:
        Shows the distribution of the time column plotted on a histogram with 100 bins
    '''
    time_stats = {}
    time_stats['min'] = data['TIME'].min()
    time_stats['max'] = data['TIME'].max()
    time_stats['mean'] = data['TIME'].mean()
    time_stats['median'] = data['TIME'].median()
    time_stats['std'] = data['TIME'].std()

    data['TIME'].hist(bins=100, color='skyblue', edgecolor='black')
    plt.title('Frequency of Entries per Day', fontsize=16)
    plt.xlabel('Time', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.grid(axis='y', alpha=0.75)
    plt.show()

    return time_stats

def conduct_hypothesis_test(data):
    # Function to conduct a hypothesis test
    pass

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    file_path = "data/processed/soc-sign-bitcoinotc-signed.csv"
    # lines = 100
    # data = pd.read_csv(file_path, nrows=lines,header=0)
    data = pd.read_csv(file_path, header=0)
    data = epoch_to_datetime(data)
    time_stats = calculate_time_statistics(data)
    print(time_stats)