'''
tested on python 3.6

This function transforms the data scraped from goodreads api into
user based dataset, and user based friends 
dataset.


data_transformation(out_args, data_input_array)

out_args:   sequence of integers, separated by commas, specifies which dataset to output,
            order is not important
            1: reader_basket_output
            2: friends_output
            3: book_basket_output
            4: books_output

Example: data_transformation('1,2,3,4', [dat1, dat2, dat3])


Output Format:
        reader_basket: {readerid: {'bookisbn13':{'name':name, 'user_rating':rating, 'avg_rating':rating},....}}
        friends: {readid: {'name':name, 'friends':  {friendsid:friends_name,...}}}
        book_basket: {'bookisbn13': [readerid,...]}
        books: {'bookisbn13':{'isbn':, 'avg_rating':, 'description':, 'name':}}
'''


import sys
import json


def data_transformation(out_args, data_input_array):
    print('------------------------------------------------------')
    input_args_len = len(data_input_array)
    
    reader_basket_output = {}
    friends_output = {}
    books_output = {}
    book_basket_output = {}
    
    med = {}
    for i in range(input_args_len):
        with open(data_input_array[i], 'r') as input:
            med = {**med, **json.load(input)}
    
    output_arr = out_args.strip().split(',')
    
    
    for key, value in med.items():
        
        friend_dict = {}
        # For friends_output
        for friend_name, friend_id in value['friends'].items():
            friend_dict[str(friend_id)] = str(friend_name)
        friends_output[key] = {'name': value['name'], 'friend': friend_dict}
        
        
        readers_basket = {}
        # For books_output, book_basket_output, reader_basket_output
        for bookname, bookinfo in value['books'].items():
            
            if type(bookinfo['isbn13']) is not dict:
                
                if str(bookinfo['isbn13']) not in books_output:
                    temp = {}
                    temp['isbn'] = bookinfo['isbn']
                    temp['avg_rating'] = bookinfo['avg_rating']
                    temp['description'] = bookinfo['description']
                    temp['name'] = bookname
                    
                    books_output[str(bookinfo['isbn13'])] = temp
                
                
                
                if str(bookinfo['isbn13']) not in book_basket_output:
                    book_basket_output[str(bookinfo['isbn13'])] = [key]
                else:
                    book_basket_output[str(bookinfo['isbn13'])].append(key)
                
                
                readers_basket[str(bookinfo['isbn13'])] = {'name' : bookname, 'user_rating' : bookinfo['user_rating'], 'avg_rating' : bookinfo['avg_rating']}
            
        reader_basket_output[str(key)] = readers_basket
    
    
    if '1' in output_arr:
        with open('reader_basket', 'w+') as output:
            json.dump(reader_basket_output, output)
            print("readers_basket length: " + str(len(reader_basket_output)))
    
    if '2' in output_arr:
        with open('friends', 'w+') as output:
            json.dump(friends_output, output)
            print("friends length: " + str(len(friends_output)))
    
    if '3' in output_arr:
        with open('book_basket', 'w+') as output:
            json.dump(book_basket_output, output)
            print("book_basket length: " + str(len(book_basket_output)))
    
    if '4' in output_arr:
        with open('books', 'w+') as output:
            json.dump(books_output, output)
            print("books length: " + str(len(books_output)))
            
