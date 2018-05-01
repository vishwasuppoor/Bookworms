import json
import sys
import os
import random
import bookworms
from heapq import nlargest


def build_links(nest, root, LINKS, DATA, MAX, booklist, book_reference, books_associated):

	if nest <= MAX:
		try:
			friend_dict = DATA[root]['friends']
			Books = DATA[root]['books']

			# print(Books)

			for book in Books:
				bookisbn = DATA[root]['books'][book]['isbn13']
				if not (bookisbn in booklist):
					booklist.append(bookisbn)

			# find_associated_book(book_reference, books_associated, booklist)

			# add source, target for root
			for friend in friend_dict:
				id = friend_dict[friend]

				LINKS.append({'source': str(DATA[root]['name']),
						  	  'target': str(friend),
						  	  'value': str(nest)
						  	})
				build_links(nest + 1, str(id), LINKS, DATA, MAX, booklist, book_reference, books_associated)
		except KeyError:
			pass
	books_recommend = find_associated_book(book_reference, books_associated, booklist)
	book_top_ten = []
	for book in books_recommend:
		#print(book)
		book_top_ten.append({'book': str(book)})
	#print(book_top_ten)
	path = os.path.dirname(bookworms.__file__)
	with open(path + '/static/book_recommenddata.json', 'w+') as b_file:
	 	json.dump(book_top_ten, b_file)

	return books_recommend

def find_associated_book(book_reference, books_associated, booklist):
		# defination
		dct = {}
		abooklist = []
		fqlist = []

		#get the name of all reference books
		# rbooks = book_reference.keys()

		#find all books associated with referenced books
		for rbook in booklist:
			# print(rbook)
			abooks = books_associated.get(str(rbook))
			# print(abooks)
			#get associated book frequency
			if abooks is not None:
				for abook in abooks:
					if not (abook in abooklist):
						if abook in book_reference:
							abookfq = abooks[abook]

							#add assoicated books and their frequency into list
							abooklist.append(str(book_reference[abook]))
							fqlist.append(str(abookfq))

		#write into dictionary
		dct = dict(zip(abooklist, fqlist))

		#print the 3 books with largest frequency
		ten_largest = nlargest(10, dct, key = dct.get)
		# print(three_largest)

		# with open('templates/allassociate.json', 'w+') as allassociate:
			# json.dump(dic, allassociate)
		return ten_largest


def loaddata(root, path, raw_data):

	# print("Loading data")
	with open(path +'/' + raw_data, 'r') as r_file:
		data = json.load(r_file)


	# print(root)
	#root = str(16506879)
	#root = str(65721667)
	#print(rand)
	if root not in data:
		print("not found, randomizing")
		no_books = True
		while no_books:
			rand = random.choice(list(data.keys()))
			root = str(rand)
			print(root)
			no_books = (len(data[root]['books']) == 0)

	#root = str(14341038)

	with open(path + 'reader_basket', 'r') as rd_file:
		reader_basket = json.load(rd_file)

	with open(path + 'book_basket', 'r') as bk_file:
		book_basket = json.load(bk_file)

	with open(path + 'friends', 'r') as fr_file:
		friends = json.load(fr_file)

	with open(path + 'books', 'r') as books:
		books = json.load(books)
		book_reference = {i: books[i]['name'] for i in books}

	with open(path + 'books_associated', 'r') as booksassociated:
		books_associated = json.load(booksassociated)

	LINKS = []
	booklist = []
	MAX = 2
	dic = []

	books = build_links(1, root, LINKS, data, MAX, booklist, book_reference, books_associated)



	return LINKS, root


def main():
	data_analyze('1')


if __name__ == '__main__':
	main()


