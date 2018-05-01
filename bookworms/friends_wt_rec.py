import sys
from sematch.semantic.similarity import WordNetSimilarity
import json
import numpy as np
import random
import math

# this script uses the sense words created by create sense words file and the raw json file to recommend books
# it takes in the user id and the query book id as the input arguments and print the global and local recommendations.
# usage - python3 friends_wt_rec.py user_id book_id

# getting most frequent words from a list
def most_frequent_words(word_list, num_of_words):
	frequencies = {}
	most_frequent_words = []
	for word in word_list:
		frequencies[word] = word_list.count(word)

	sorted_word_list = sorted(word_list, key=frequencies.__getitem__)
	most_frequent_words = sorted_word_list[-num_of_words:]
	return most_frequent_words 

# function to store sense words, for every isbn, in a dictionary from the sense words file
def store_sense_words(file):
	sense_words = {}
	for line in file:
		fields = line.rstrip().split("\t")
		isbn = fields[0]
		if isbn not in sense_words:
			sense_words[isbn] = fields[1].split(" ")
	return sense_words

# filter books based on the average ratings and randomly sample 2000 books
def filter_books(data):
	ratings = {}
	filtered_books = {}
	for data_point in data:
		for book in data[data_point]["books"]:
			ratings[str(data[data_point]["books"][book]["isbn"])] = float(data[data_point]["books"][book]["avg_rating"])

	x=list(ratings.values()) #get the ratings (values) as a list
	global_average_rating = sum(x)/len(x)
	p80= np.percentile(x, 80) #cutoff for 80th percentile

	for key, value in ratings.items():
		if (value < p80):
			filtered_books[key] = value

	isbns=list(filtered_books.keys()) #get the isbns (keys) as a list	
	possibilities = 2000
	# print(len(filtered_books))
	selected_isbns = random.sample(isbns, possibilities)

	return selected_isbns

# remove "_" characters from the words
def create_clean_list(word_list):
	for word in word_list:
		if ("_" in word):
			for splitted_word in word.split("_"):
				word_list.append(splitted_word)
	return word_list

# create Candidate books set
def candidate_books_set(query_book, sense_words, filtered_books, book_names):
	books_scores = {}
	query_words = create_clean_list(sense_words[query_book])
	books = []
	query_word_cloud = query_words
	names = []
	for isbn in filtered_books:
		count = 0
		total_score = 0
		if ((isbn != query_book) and (isbn not in books_scores)):
			for tag in query_word_cloud:
				for tag_2 in create_clean_list(sense_words[isbn]):
					score = round(wns.word_similarity(tag,tag_2),5)
					if (score > 0.30):
						count += 1
						total_score += score 
						break
				if (count == 10):
					books_scores[isbn] = total_score
					books.append(isbn)
					break
		if (len(books_scores) == 50):
			break
	sorted_books = sorted(books, key=books_scores.__getitem__)
	candidate_book_set = sorted_books
	scores = []
	for book in candidate_book_set:
		scores.append(books_scores[book])
	for i in range(10):
		names.append(book_names[sorted_books[-i]]["name"])
	return candidate_book_set, names ,score

# create a friend list for the user
def create_friend_list(user, data_file):
	friend_list = []
	for key, value in data_file[user]["friends"].items():
		friend_list.append(value)
	return friend_list

# store all the books of a friend corresponding to his id 
def friends_books(friend_list, data_file):
	friends_books = {}
	for friend in friend_list:
		if (str(friend) not in data_file):
			continue
		for book in (data_file[str(friend)]["books"]):
			if ((type(data_file[str(friend)]["books"][book]["isbn"]) is str)):
				friends_books[friend] = data_file[str(friend)]["books"][book]["isbn"]
	return friends_books

# remove the friends, if number of books is less than 10 in his bucket, to be considered for closeness
def friend_cutter(friends_books):
	filtered_friends = []
	for key, value in friends_books.items():
		if (len(value) >= 10):
			filtered_friends.append(key)
	return filtered_friends

# create a most frequent words list for a friend from all his books
def create_friends_word_cloud(friend_list, sense_words):
	friends_word_cloud = {}
	for friend in friend_list:
		friends_word_cloud[friend] = []
		if (str(friend) not in data_file):
			continue
		for book in (data_file[str(friend)]["books"]):
			if ((type(data_file[str(friend)]["books"][book]["isbn"]) is str)):
				friends_word_cloud[friend] = friends_word_cloud[friend]+(sense_words[data_file[str(friend)]["books"][book]['isbn']])
		friends_word_cloud[friend] = most_frequent_words(friends_word_cloud[friend],100)
	return friends_word_cloud

# calculate closeness of a friend for a particular book
def calculate_closeness_score(friend_list, query_word_cloud, friends_word_cloud):
	friend_closeness = {}
	for friend in friend_list:
		closenss_score = 0
		if (str(friend) not in data_file):
			continue
		for tag_1 in query_word_cloud:
			for tag_2 in create_clean_list(friends_word_cloud[friend]):
				if (round(wns.word_similarity(tag_1,tag_2),2) >= 0.30):
					closenss_score += 1
		friend_closeness[friend] = round((closenss_score/(len(query_word_cloud)*len(friends_word_cloud)))*10,4)
	return friend_closeness

# recommend books by weighting the similarity scores with friends closeness score
def recommend_books(friends_word_cloud, candidate_books, scores, sense_words, friends_closeness):
	total_recommendation_scores = {}
	candidates = []
	for i in range(len(candidate_books)):
		book = candidate_books[i]
		candidates.append(book)
		query_word_cloud = most_frequent_words(sense_words[book],20)
		recommendation_score = 0
		for friend, cloud in friends_word_cloud.items():
			count = 0
			for tag_1 in query_word_cloud:
				for tag_2 in cloud:
					if (round(wns.word_similarity(tag_1,tag_2),2) >= 0.30):
						count += 1
			score = friends_closeness[friend]*count
			if (score > recommendation_score):
				recommendation_score = score
		total_recommendation_scores[book] = recommendation_score
		# print(recommendation_score)

	recommended_books = sorted(candidates, key=total_recommendation_scores.__getitem__)
	return recommended_books

def rec_books(user, book, path, raw_data):
	with open(path +'/' + raw_data, 'r') as r_file:
			data = json.load(r_file)

	wns = WordNetSimilarity()

	file = open(path+"win_sense_words.txt",'r')
	json_file = open(path +'/' + raw_data, 'r')
	data_file = json.load(json_file)

	book_file = open(path + 'books','r')
	book_names = json.load(book_file)

	query_book = book


	sense_words = store_sense_words(file)
	friend_list = create_friend_list(user, data_file)
	query_word_cloud = sense_words[query_book]
	# print(len(query_word_cloud))

	filtered_books = filter_books(data_file)
	candidate_books, global_book_names, scores = candidate_books_set(query_book, sense_words, filtered_books,book_names)
	print("\nGlobal Recommendations\n")
	# print(candidate_books)
	print(global_book_names)

	# print(len(candidate_books))

	friend_books = friends_books(friend_list, data_file)
	filtered_friends = friend_cutter(friend_books)
	friends_word_cloud = create_friends_word_cloud(filtered_friends, sense_words)

	friends_closeness = calculate_closeness_score(filtered_friends, query_word_cloud, friends_word_cloud)
	# print(len(filtered_friends))
	# print(calculate_closeness_score(filtered_friends, query_word_cloud, friends_word_cloud))
	recommended_list = recommend_books(friends_word_cloud, candidate_books, scores, sense_words, friends_closeness)
	local_book_names = []

	print("\n Local Recommendations:\n")
	# print(recommended_list)
	for i in range(10):
		local_book_names.append(book_names[recommended_list[-i]]["name"])
	print(local_book_names)

# print(create_candidate_book_set(query_word_cloud, friends_books))
# print(query_word_cloud(query_word_cloud, friends_books))



