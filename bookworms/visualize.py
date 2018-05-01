'''
Tested on python 3.6

This function visualizes the data from data transformation and
training. If no training and data transformation is done previously,
this function will load sample dataset, which is 100 readers.

Usage:

python visualize
'''


import sys, os
import random
import json
from subprocess import call
import bookworms


def visualize(input_file, run_dir):
    # visualize() takes one input argument, as intput argument should be generated
    # from the training process. If train is not called, visualize() will use the 
    # predownloaded data for visualization
    
    try:
        # open input raw data
        with open(input_file[0]) as file:
            pass
        input_str = input_file
    except:
        print('------------------------------------------------------')
        print('No input file is specified. Using sample_data instead.')
        script_dir = os.path.dirname(__file__)
        rel_path = 'sample_data'
        file_name = 'input_100.json'
        sample_data_path = os.path.join(script_dir, rel_path, file_name)
        input_str = [file_name]

    try:
        # open input data
        with open('reader_basket', 'r') as input:
            reader_basket = json.load(input)

        data_path = run_dir
        print(data_path)
        
    except:
        # if no input data is generated, sample data from the folder 'sample_data'
        # will be used
        print('------------------------------------------------------')
        print('No input "reader_basket" file is found. Using sample_data instead.')
        script_dir = os.path.dirname(__file__)
        rel_path = 'sample_data'
        file_name = 'reader_basket'
        sample_data_path = os.path.join(script_dir, rel_path, file_name)
        # open the file
        with open(sample_data_path, 'r') as input:
            reader_basket = json.load(input)

        data_path = os.path.join(script_dir, rel_path)
        
    # get the users and generate one random user    
    users = list(reader_basket.keys())
    random_user = random.choice(users)
    
    # prepare for the flask website visulization
    print('Setting web page for visualization')
    assert sys.version_info >= (3,6)
    py_ver = str(sys.executable)
    path = os.path.dirname(bookworms.visualize.__file__)
    print(path)
    call([py_ver, path + '/app.py', data_path, input_str[0]])
    
def main():
    visualize(['aslfd'])

if __name__ == '__main__':
    main()