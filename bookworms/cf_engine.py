import json
import math

class cf_engine(object):
    def __init__(self,**kwargs):
        self.dataset = 'sample_data/input_100.json'
        self.match = 2
        self.kNN = 20
        self.recos = 5
        self.min_books = 2
        self.test_size = 0.5
        try:
            self.dataset = kwargs['dataset']
        except:
            pass
        try:
            self.min_books = kwargs['min_books']
        except:
            pass       
        try:
            self.match = kwargs['match']
        except:
            pass
        try:
            self.kNN = kwargs['kNN']
        except:
            pass
        try:
            self.recos = kwargs['recos']
        except:
            pass
        try:
            self.test_size = kwargs['test_size']
        except:
            pass
        self.load_data(self.min_books)
        try:
            self.user = kwargs['user']
            self.user_prep(self.user)
        except:
            self.engine_perf()

    def load_data(self,min_books):
        with open(self.dataset,'r') as data_file:  
            data = json.load(data_file)
            self.people_data = {}
            self.isbn_match = {}
            for k,v in data.items():
                num_books = 0
                for x,y in v['books'].items():
                    if isinstance(y['isbn13'], str):
                        num_books += 1
                if num_books >= self.min_books:
                    for x,y in v['books'].items():
                        if isinstance(y['isbn13'], str):
                            self.isbn_match[y['isbn13']] = x
                            try:
                                self.people_data[k].update({y['isbn13']:y['user_rating']})
                            except:
                                self.people_data[k] = {y['isbn13']:y['user_rating']}
    
    def user_prep(self,user):
        self.user = user
        self.user_data = self.people_data[user]
        self.test_data = {}
        self.train_data = {}
        num_books = len(self.people_data[user])
        if num_books > 1:
            i = 0
            for book in self.user_data:
                if i < round(self.test_size*num_books):
                    self.test_data[book] = self.user_data[book]
                else:
                    self.train_data[book] = self.user_data[book]
                i += 1

    def get_similar_users(self,user_data):
        self.user_basket = []
        self.similar = []
        for book in user_data:
            self.user_basket.append(book)
        for person in self.people_data:
            if person != self.user:
                count = 0
                for book in self.user_basket:
                    if book in self.people_data[person].keys():
                        count += 1
                if count >= self.match:
                    self.similar.append(person)
                    
    def get_mean_rating(self,user_data,people_list):
        self.mean_ratings = {}
        self.book_basket = {}
        ratings = 0
        books = 0
        for book in user_data:
            ratings += user_data[book]
            books += 1
        self.mean_ratings[self.user] = ratings/books
        for person in people_list:
            ratings = 0
            books = 0
            for book in self.people_data[person].keys():
                self.book_basket[book] = 0
                ratings += self.people_data[person][book]
                books += 1
            self.mean_ratings[person] = ratings/books
            
    def get_normalized_ratings(self,user_data,people_list):
        self.get_mean_rating(user_data,people_list)
        self.normalized_ratings = {}
        for book in user_data:
            try:
                self.normalized_ratings[self.user].update({book:user_data[book] - self.mean_ratings[self.user]})
            except:
                self.normalized_ratings[self.user] = {book:user_data[book] - self.mean_ratings[self.user]}            
        for person in people_list:
            for book in self.people_data[person].keys():
                try:
                    self.normalized_ratings[person].update({book:self.people_data[person][book] - self.mean_ratings[person]})
                except:
                    self.normalized_ratings[person] = {book:self.people_data[person][book] - self.mean_ratings[person]}
    
    def cosine_similarity(self,user_data,people_list):
        user_norm = 0
        self.similarity = {}
        
        for book in user_data:
            rating = self.normalized_ratings[self.user][book]
            user_norm += rating*rating
        user_norm = math.sqrt(user_norm)
        
        for person in people_list:
            dot = 0
            person_norm = 0
            for book in self.people_data[person].keys():
                rating = self.normalized_ratings[person][book]
                person_norm += rating*rating
                if book in user_data:
                    dot += self.normalized_ratings[self.user][book]*rating            
            person_norm = math.sqrt(person_norm)
            try:
                simil = dot/(user_norm*person_norm)
            except:
                simil = 0
            self.similarity[person] = simil
    
    def select_kNN(self,similarity_scores):
        if len(similarity_scores) < self.kNN:
            similar_users = len(similarity_scores)
        else:
            similar_users = self.kNN
        sorted_similarity = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
        self.neighbours = sorted_similarity[0:similar_users]
        self.similarity_sum = 0
        for v in self.neighbours:
            if v[1] > 0:
                self.similarity_sum += v[1]
    
    def predict(self,user_data):
        self.get_similar_users(user_data)
        self.get_normalized_ratings(user_data,self.similar)
        self.cosine_similarity(user_data,self.similar)
        self.select_kNN(self.similarity)
        self.prediction_basket = {}
        self.prediction = []
        for neighbour in self.neighbours:
            person = neighbour[0]
            if self.similarity[person] > 0:
                simil = self.similarity[person]
                for book in self.people_data[person].keys():
                    self.book_basket[book] += simil * self.normalized_ratings[person][book]
        for book in self.book_basket:
            try:
                self.prediction_basket[book] = self.mean_ratings[self.user] + self.book_basket[book]/self.similarity_sum
            except:
                self.prediction_basket[book] = self.mean_ratings[self.user]
        self.sorted_prediction = sorted(self.prediction_basket.items(), key=lambda x: x[1], reverse=True)
        if len(self.prediction_basket) < self.recos:
            op_num = len(self.prediction_basket)
        else:
            op_num = self.recos
        for i in range(op_num):
            self.prediction.append({'book':self.isbn_match[self.sorted_prediction[i][0]]})
        return self.prediction

    def RMSE(self,user_data,prediction):
        squared_sum = 0
        count = 0
        for book in user_data:
            if book in prediction:
                difference = prediction[book] - user_data[book]
                squared_sum += difference*difference
                count += 1
        try:
            return math.sqrt(squared_sum/count)
        except:
            return 'no match'
    
    def MAE(self,user_data,prediction):
        abs_sum = 0
        count = 0
        for book in user_data:
            if book in prediction:
                difference = prediction[book] - user_data[book]
                abs_sum += abs(difference)
                count += 1
        try:
            return abs_sum/count
        except:
            return 'no match'
        
    def test_stats(self,user_data,prediction):
        avg_rating = self.mean_ratings[self.user]
        matching_predictions = 0
        true_positive = 0
        true_negative = 0
        false_positive = 0
        false_negative = 0
        for book in user_data:
            if book in prediction:
                matching_predictions += 1
                if (user_data[book] - avg_rating) >= 0 and (prediction[book] - avg_rating) >= 0:
                    true_positive += 1
                elif (user_data[book] - avg_rating) < 0 and (prediction[book] - avg_rating) < 0:
                    true_negative += 1
                elif (user_data[book] - avg_rating) < 0 and (prediction[book] - avg_rating) >= 0:
                    false_positive += 1
                elif (user_data[book] - avg_rating) >= 0 and (prediction[book] - avg_rating) < 0:
                    false_negative += 1
        coverage = matching_predictions/len(user_data)
        try:
            hit_rate = matching_predictions/len(prediction)
        except:
            hit_rate = 0
        try:
            accuracy = (true_positive + true_negative)/matching_predictions
        except:
            accuracy = 0
        try:
            precision = true_positive/(true_positive + false_positive)
        except:
            precision = 0
        try:
            recall = true_positive/(true_positive + false_negative)
        except:
            recall = 0
        return accuracy,precision,recall,coverage,hit_rate
    
    def engine_perf(self):
        self.recos = 0
        size = len(self.people_data)
        num_users = size
        total_RMSE = 0
        total_MAE = 0
        total_accuracy = 0
        total_precision = 0
        total_recall = 0
        total_coverage = 0
        total_hit_rate = 0
        j = 0
        print('Number of users in dataset =',size)
        print('Training')
        for person in self.people_data:
            j += 1
            print('.',end='')
            if j % int(num_users/ 10) == 0:
                print(j)
            self.user_prep(person)
            self.predict(self.train_data)
            flag = 0
            try:
                accuracy = self.test_stats(self.test_data,self.prediction_basket)[0]
                precision = self.test_stats(self.test_data,self.prediction_basket)[1]
                recall = self.test_stats(self.test_data,self.prediction_basket)[2]
                coverage = self.test_stats(self.test_data,self.prediction_basket)[3]
                hit_rate = self.test_stats(self.test_data,self.prediction_basket)[4]
                total_RMSE += self.RMSE(self.test_data,self.prediction_basket)
                total_MAE += self.MAE(self.test_data,self.prediction_basket)
                flag = 1
            except:
                size -= 1
            if flag == 1:
                total_accuracy += accuracy
                total_precision += precision
                total_recall += recall
                total_coverage += coverage
                total_hit_rate += hit_rate
        overall_RMSE = total_RMSE/size
        overall_MAE = total_MAE/size
        overall_accuracy = total_accuracy/size
        overall_precision = total_precision/size
        overall_recall = total_recall/size
        overall_coverage = total_coverage/size
        overall_hit_rate = total_hit_rate/size
        with open('engine_evaluation.txt', 'w') as f:
            f.write('RMSE ='+str(overall_RMSE)+'\n')
            f.write('MAE ='+str(overall_MAE)+'\n')
            f.write('accuracy ='+str(overall_accuracy)+'\n')
            f.write('precision ='+str(overall_precision)+'\n')
            f.write('recall ='+str(overall_recall)+'\n')
            f.write('coverage ='+str(overall_coverage)+'\n')
            f.write('hit_rate ='+str(overall_hit_rate)+'\n')
            f.write('number of valid recommendations ='+str(size)+'\n')