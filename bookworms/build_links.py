import json
import sys
import random


def build_links(nest, root, LINKS, DATA, MAX):
	#print(DATA[root]['name'])
	print(root in DATA)
	if nest <= MAX:
		try: 
			friend_dict = DATA[root]['friends']
			# add source, target for root
			for friend in friend_dict:
				id = friend_dict[friend]
				LINKS.append({'source': str(DATA[root]['name']),
						  	  'target': str(friend),
						  	  'value': str(nest)
						  	})
				build_links(nest + 1, str(id), LINKS, DATA, MAX)
		except KeyError:
			pass

def top_n_max_readers(root, n, BOOKS, USERS):
	book_list_lens = []
	for book_id, book_info in USERS[root].items():
		book_list_lens.append((len(BOOKS[book_id]), (book_id, book_info['name'])))

	book_list_lens = (sorted(book_list_lens))
	try:
		lens, ids = zip(*book_list_lens)
		return(ids[-n:])
	except ValueError:
		print("No books for this user!")
		return([])


def build_book_links(root, bLINKS, BOOKS, USERS, FRIENDS):
	u_size = 30
	b_size = 7
	filtered = top_n_max_readers(root, b_size, BOOKS, USERS)
	#Limit to 10 books per root user
	for book_id, book_name in filtered:
		bLINKS.append({ 'source': FRIENDS[root]['name'],
						'target': book_name,
						'value': 1
						})
		# 
		# Limit to 30(?) users per book
		users_per_book = 0
		for user in (BOOKS[book_id]):
			if users_per_book == u_size:
				break
			if user in FRIENDS[root]['friend']:
				val = 2
			else:
				val = 3
			bLINKS.append({ 'source': FRIENDS[user]['name'],
						'target': book_name,
						'value': val
						})
			users_per_book += 1


def data_analyze(root, path):
	with open(path + 'reader_basket', 'r') as rd_file:
		reader_basket = json.load(rd_file)

	with open(path + 'book_basket', 'r') as bk_file:
		book_basket = json.load(bk_file)

	with open(path + 'friends', 'r') as fr_file:
		friends = json.load(fr_file)


	if root not in friends:
		print("not found, randomizing root")
		rand = random.choice(list(friends.keys()))
		root = str(rand)
	print("Loading data")

	print(root)
	#root = str(16506879)
	#root = str(65721667)
	#print(rand)



	print("Found user")
	print(friends[root]['name'])
	#LINKS = []
	bLINKS = []
	MAX = 10
	#tree = build_book_nest(root, book_basket, reader_basket, friends, data)
	#print(tree)
	# with open('static/book_tree.json', 'w+') as t_file:
	# 	json.dump(tree, t_file)
	# build_links(1, root, LINKS, data, MAX)
	# print(bLINKS)
	# with open('links.json', 'w+') as p_file:
	#  	json.dump(LINKS, p_file)
	print("Analyzing")
	build_book_links(root, bLINKS, book_basket, reader_basket, friends)
	# with open('static/book_links.json', 'w+') as b_file:
	#  	json.dump(bLINKS, b_file)
	return bLINKS

def main():
	data_analyze('1')

if __name__ == '__main__':
	main()


