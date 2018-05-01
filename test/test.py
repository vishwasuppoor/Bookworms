from bookworms.train import train
from bookworms.visualize import visualize
import os

def test():
    print('training input json')
    train(['input.json'], 10, 5)
    
    print('')
    print('when no input file is specified')
    train([], 10, 5)
    
    print('')
    print('visualize')
    visualize(['input.json'], os.getcwd())


if __name__ == '__main__':
    test()
    
