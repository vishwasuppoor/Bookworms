'''
List of utility functions

suppress_stdout() suppresses the print() function temporarily

'''

from contextlib import contextmanager
import os, sys


# suppress output method
@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout
