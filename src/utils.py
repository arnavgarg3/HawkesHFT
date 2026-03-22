import pandas as pd
import numpy as numpy
import binance_historical_data as bhd


'''
Load in the data from Binance at
'''
def load_data(file_path):

	df = read_csv(file_path)
