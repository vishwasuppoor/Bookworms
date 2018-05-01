'''
Tested on python 3.6

This function creates recommendation based readers basket, 
counting frequencies of pairs of books, using association rule
mining.

These pairs already eliminates the low frequency appearances, 
support will be the eliminating factor

Usage: fast_fpv2(support_value, input, suppress_output)

Input:
support_value: specify the lower limit of appearances 
    for books to be counted into pairs
input: reader_basket generated from previous data procession
suppress_output: whether to show the calculation process

Output:
books_associated_{support}: json, {'isbn1':{'isbn': incidents, ...}, ...}
books_associated_{support}_small_{small_size}: json,
    {'isbn1':{'isbn': incidents, ...}, ...}, length of each key-value
    pair is restricted to 20
'''

from .util import suppress_stdout
import json, csv, sys, os
import collections
import numpy as np
import time
import operator


def fast_fp(support_value, data_input, sup):
    print('------------------------------------------------------')
    print('start association rule mining:')
    t1 = time.time()
    if sup:
        with suppress_stdout():
            fast_fpv2(support_value, data_input)
    else:
        fast_fpv2(support_value, data_input)
    print('finished after ' + '{0:.3f}'.format(time.time() - t1) + ' s.')
    
    
def fast_fpv2(support_value, data_input):
    
    # size of the recommended books for each book
    small_res_size = 20

    t1 = time.time()
    print('starting at time:')
    print(time.time()- t1)



    print('load dataset')
    with open(str(data_input), "r") as input:
        dat = json.load(input)

    print('time at completion:')
    print(time.time()- t1)
    print('\n\n\n')


    # getting support
    support = int(support_value)



    print('getting all incidents list:')
    # json file has an array in it, reader basket
    incid = []
    for key, val in dat.items():
        incid.extend(val)

    print('time at completion:')
    print(time.time()- t1)
    print('\n\n\n')



    # get frequency of all books
    counter = collections.Counter(incid)
    print('number of books')
    print(len(counter))

    print('median of frequency is')
    print(np.median([value for key, value \
        in dict(counter).items()]))

    print('average of frequency is')
    print(np.mean([value for key, value \
        in dict(counter).items()]))

    # get high frequency books
    counter_high = [key for key, value \
        in dict(counter).items() if value >= support]
    print('number of high frequency books')
    print(len(counter_high))
    print('\n\n\n')


    print('creating new reader basket')
    size_b = len(dat)
    print('size of baskets: ' + str(size_b))

    # this utility is just for monitoring the result
    inc = int(size_b / 20) if int(size_b / 20) > 1 else 1
    ind = list(range(0, size_b, inc))
    if ind[-1] != size_b:
        ind.append(size_b)

    # analyse the json data pair by pair
    # firstly remove the infrequent books
    # then for each pair, write the results into the corresponding
    # dict position
    res_t = {}
    for ii in range(len(ind) - 1):
        for key, val_t in list(dat.items())[ind[ii]:ind[ii + 1]]:
            val = [i for i in val_t if i in counter_high]
            for i in val:
                if i in res_t:
                    for j in val:
                        if j in res_t[i]:
                            res_t[i][j] += 1
                        else:
                            res_t[i][j] = support + 1
                else:
                    temp = {}
                    for j in val:
                        temp[j] = support + 1
                    res_t[i] = temp
        print('{0:.3f} completed {1:.3f} s elapsed'\
            .format(ind[ii + 1] / size_b, time.time()- t1))

    print('time at completion:')
    print(time.time()- t1)
    print('\n\n\n')


    print('remove self nodes')
    for key, value in res_t.items():
        res_t[key].pop(key, None)
    print('time at completion:')
    print(time.time()- t1)
    print('\n\n\n')


    print('saving data')
    with open('books_associated_s=' + str(support), "w+") as output:
        json.dump(res_t, output)
    print('time at completion:')
    print(time.time()- t1)
    print('\n\n\n')


    print('saving data (small books ' + str(small_res_size) + ')')
    res_t_small = {}
    for key, value in res_t.items():
        # get the size of the recommended books
        d = len(value) if len(value) < small_res_size else small_res_size
        sorted_value = sorted(value.items(), \
            key = operator.itemgetter(1), reverse = True)
        sorted_value = sorted_value[:d]
        res_t_small[key] = dict(sorted_value)
    with open('books_associated_s=' + str(support) + '_small_' \
        + str(small_res_size), "w+") as output:
        json.dump(res_t_small, output)
    with open('books_associated', "w+") as output:
        json.dump(res_t_small, output)
    print('time at completion:')
    print(time.time()- t1)
    print('\n\n\n')
    
    
