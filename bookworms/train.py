'''
Tested on python 3.6

This function trains the data input.
First it transform the data into 4 subdatasets.
Then it trains the data using separate algorithms, currently only ARM is used.

Usage:

python train input_data

'''

import sys, os
from .data_tsf import data_transformation
from .fast_fp import fast_fp

def train(input_list, us_support, variable):
    # input is in the format of a list, ['input1', 'input2', ...]
    # us_support is user defined support for ARM
    # variable is the arbitrary variable defined in __main__.py
    
    # getting input data
    try:
        if len(input_list) < 1:
            raise Exception('No input file')
        input_str = []
        for i in range(len(input_list)):
            input_str.append(input_list[i])
        
    except:
        print('------------------------------------------------------')
        print('No input file is specified. Using sample_data instead.')
        script_dir = os.path.dirname(__file__)
        rel_path = 'sample_data'
        file_name = 'input_100.json'
        sample_data_path = os.path.join(script_dir, rel_path, file_name)
        input_str = [sample_data_path]
    
    support = us_support
    
    # transform the data
    data_transformation('1,2,3,4', input_str)

    # train the collaborative filtering


    # train the ricky's algorithm
    
    
    # train the ASM
    fast_fp(support, 'reader_basket', True)
    
