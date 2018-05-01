'''
Implementation of the script usage

The main function takes three arguments:
functionality: train or v
-f: directory to file name
-s: support for ARM training
'''

import os
import sys
import json
import argparse
import shutil
import bookworms

# Using python defined argument parser
parser = argparse.ArgumentParser(description = 'bookworms portal')
parser.add_argument('functionality', help = 'Actions that can be done. Actions are: train (t), visualize (v)')
parser.add_argument('-f', '--file', nargs = '*', 
                    dest = 'file', help = 'The files that are used for training')

parser.add_argument('-s', '--support', dest = 'support',
                    help = 'set up support for ARM training',
                    default = 10, type = int)

# If you need more argument(s), change the following line into what you need or add
# another line if you need more than 2 arguments
parser.add_argument('-v', # name for the argument
                    '--variable', # long name for the argument
                    dest = 'variable', # the name you use for accessing the variable from args
                    help = 'set up an arbitrary variable', # help message when type in -h for help
                    default = 5, # defualt value is set to 5
                    type = int)

args = parser.parse_args()

if args.functionality == 'train' or args.functionality == 't':
    from .train import train
    train(args.file, args.support, args.variable)
    
if args.functionality == 'visualize' or args.functionality == 'v':
    from .visualize import visualize
    if not bool(args.file):
        path = os.path.dirname(bookworms.__file__)
        print(path)
        shutil.copyfile(path + '/' + 'sample_data/input_100.json', os.getcwd() + '/input_100.json')
    visualize(args.file, os.getcwd())
    
    
if args.variable > 0:
    print('')
