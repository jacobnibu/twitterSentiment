#!/usr/bin/env python
import os, sys, json, pickle, happybase, logging, datetime, socket
#import config
#from naive_bayes_classifier import NaiveBayesClassifier
#from functions import *
#import methods

'''
try:
    connection = happybase.Connection('localhost')
    table = connection.table('tweets')
    machine_name = socket.gethostname()
except:
    None
'''
# ==========================================================
# classifier helper class
# ==========================================================
import re
import nltk
from nltk.classify import *

class ClassifierHelper:
    #start __init__
    def __init__(self, featureListFile):
        self.wordFeatures = []
        # Read feature list
        inpfile = open(featureListFile, 'r')
        line = inpfile.readline()        
        while line:
            self.wordFeatures.append(line.strip())
            line = inpfile.readline()
    #end    

    #start extract_features
    def extract_features(self, document):
        document_words = set(document)
        features = {}
        for word in self.wordFeatures:
            word = self.replaceTwoOrMore(word) 
            word = word.strip('\'"?,.')
            features['contains(%s)' % word] = (word in document_words)
        return features
    #end

    #start replaceTwoOrMore
    def replaceTwoOrMore(self, s):
        # pattern to look for three or more repetitions of any character, including
        # newlines.
        pattern = re.compile(r"(.)\1{1,}", re.DOTALL) 
        return pattern.sub(r"\1\1", s)
    #end

    def getSVMFeatureVectorAndLabels(self, tweets):
        sortedFeatures = sorted(self.wordFeatures)
        map = {}
        feature_vector = []
        labels = []
        for t in tweets:
            label = 0
            map = {}
            #Initialize empty map
            for w in sortedFeatures:
                map[w] = 0
            
            tweet_words = t[0]
            tweet_opinion = t[1]
            #Fill the map
            for word in tweet_words:
                word = self.replaceTwoOrMore(word) 
                word = word.strip('\'"?,.')
                if word in map:
                    map[word] = 1
            #end for loop
            values = map.values()
            feature_vector.append(values)
            if(tweet_opinion == 'positive'):
                label = 0
            elif(tweet_opinion == 'negative'):
                label = 1
            elif(tweet_opinion == 'neutral'):
                label = 2
            labels.append(label)            
        return {'feature_vector' : feature_vector, 'labels': labels}
    #end
    
    #start getSVMFeatureVector
    def getSVMFeatureVector(self, tweets):
        sortedFeatures = sorted(self.wordFeatures)
        map = {}
        feature_vector = []
        for t in tweets:
            label = 0
            map = {}
            #Initialize empty map
            for w in sortedFeatures:
                map[w] = 0
            #Fill the map
            for word in t:
                if word in map:
                    map[word] = 1
            #end for loop
            values = map.values()
            feature_vector.append(values)                    
        return feature_vector
    #end
    
    #start process_tweet
    def process_tweet(self, tweet):
        #Conver to lower case
        tweet = tweet.lower()
        #Convert https?://* to URL
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
        #Convert @username to AT_USER
        tweet = re.sub('@[^\s]+','AT_USER',tweet)    
        #Remove additional white spaces
        tweet = re.sub('[\s]+', ' ', tweet)
        #Replace #word with word
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
        #trim
        tweet = tweet.strip()
        #remove first/last " or 'at string end
        tweet = tweet.rstrip('\'"')
        tweet = tweet.lstrip('\'"')
        return tweet
    #end 
    
    #start is_ascii
    def is_ascii(self, word):
        return all(ord(c) < 128 for c in word)
    #end
#end class

# =======================================================================
# naive bayes class
# =======================================================================
import nltk.classify
import re, csv
#import classifier_helper
# import html_helper

#start class
class NaiveBayesClassifier:
    """ Naive Bayes Classifier """
    #variables    
    #start __init__
    def __init__(self, data, keyword, time, trainingDataFile, classifierDumpFile, trainingRequired = 0):
        #Instantiate classifier helper        
        self.helper = ClassifierHelper('feature_list.txt')
        
        self.lenTweets = len(data)
        self.origTweets = self.getUniqData(data)
        #self.origTweets = data
        self.tweets = self.getProcessedTweets(self.origTweets)

        self.results = {}
        self.neut_count = [0] * self.lenTweets
        self.pos_count = [0] * self.lenTweets
        self.neg_count = [0] * self.lenTweets
        self.trainingDataFile = trainingDataFile

        self.time = time
        self.keyword = keyword
        #self.html = html_helper.HTMLHelper()
        
        #call training model
        if(trainingRequired):
            self.classifier = self.getNBTrainedClassifer(trainingDataFile, classifierDumpFile)
        else:
            f1 = open(classifierDumpFile)            
            if(f1):
                self.classifier = pickle.load(f1)                
                #f1.close()
                #logging.info('Successfully loaded the trained model')
            #else:
                #None
                #logging.info('Could not load the trained model; starting to train a new model...')
#                self.classifier = self.getNBTrainedClassifer(trainingDataFile, classifierDumpFile)
    #end

    #start getUniqData
    def getUniqData(self, data):
        uniq_data = {}        
        for i in range(len(data)):
            d = data[i]
            u = []
            for element in d:
                if element not in u:
                    u.append(element)
            #end inner loop
            uniq_data[i] = u            
        #end outer loop
        return uniq_data
    #end
    
    #start getProcessedTweets
    def getProcessedTweets(self, data):        
        tweets = {}        
        for i in range(len(data)):
            d = data[i]
            tw = []
            for t in d:
                tw.append(self.helper.process_tweet(t))
            tweets[i] = tw            
        #end loop
        return tweets
    #end
    
    #start getNBTrainedClassifier
    def getNBTrainedClassifer(self, trainingDataFile, classifierDumpFile):        
        # read all tweets and labels
        tweetItems = self.getFilteredTrainingData(trainingDataFile)
        
        tweets = []
        for (words, sentiment) in tweetItems:
            words_filtered = [e.lower() for e in words.split() if(self.helper.is_ascii(e))]
            tweets.append((words_filtered, sentiment))
                    
        training_set = nltk.classify.apply_features(self.helper.extract_features, tweets)
        # Write back classifier and word features to a file
        classifier = nltk.NaiveBayesClassifier.train(training_set)
        outfile = open(classifierDumpFile, 'wb')        
        pickle.dump(classifier, outfile)        
        outfile.close()        
        return classifier
    #end
    
    #start getFilteredTrainingData
    def getFilteredTrainingData(self, trainingDataFile):
        fp = open( trainingDataFile, 'rb' )
        min_count = self.getMinCount(trainingDataFile)  
        min_count = 40000
        neg_count, pos_count, neut_count = 0, 0, 0
        
        reader = csv.reader( fp, delimiter=',', quotechar='"', escapechar='\\' )
        tweetItems = []
        count = 1       
        for row in reader:
            processed_tweet = self.helper.process_tweet(row[1])
            sentiment = row[0]
            
            if(sentiment == 'neutral'):                
                if(neut_count == int(min_count)):
                    continue
                neut_count += 1
            elif(sentiment == 'positive'):
                if(pos_count == min_count):
                    continue
                pos_count += 1
            elif(sentiment == 'negative'):
                if(neg_count == min_count):
                    continue
                neg_count += 1
            
            tweet_item = processed_tweet, sentiment
            tweetItems.append(tweet_item)
            count +=1
        #end loop
        return tweetItems
    #end 

    #start getMinCount
    def getMinCount(self, trainingDataFile):
        fp = open( trainingDataFile, 'rb' )
        reader = csv.reader( fp, delimiter=',', quotechar='"', escapechar='\\' )
        neg_count, pos_count, neut_count = 0, 0, 0
        for row in reader:
            sentiment = row[0]
            if(sentiment == 'neutral'):
                neut_count += 1
            elif(sentiment == 'positive'):
                pos_count += 1
            elif(sentiment == 'negative'):
                neg_count += 1
        #end loop
        return min(neg_count, pos_count, neut_count)
    #end

    #start classify
    def classify(self):        
        for i in self.tweets:
            tw = self.tweets[i]
            count = 0
            res = {}
            for t in tw:
                label = self.classifier.classify(self.helper.extract_features(t.split()))
                if(label == 'positive'):
                    self.pos_count[i] += 1
                elif(label == 'negative'):                
                    self.neg_count[i] += 1
                elif(label == 'neutral'):                
                    self.neut_count[i] += 1
                result = {'text': t, 'tweet': self.origTweets[i][count], 'label': label}
                res[count] = result
                count += 1
                print '%s\t%s' % (label, t)
            #end inner loop
            self.results[i] = res
        #end outer loop
    #end

    #start accuracy
    def accuracy(self):
        tweets = self.getFilteredTrainingData(self.trainingDataFile)
        total = 0
        correct = 0
        wrong = 0
        self.accuracy = 0.0
        for (t, l) in tweets:
            label = self.classifier.classify(self.helper.extract_features(t.split()))
            if(label == l):
                correct+= 1
            else:
                wrong+= 1
            total += 1
        #end loop
        self.accuracy = (float(correct)/total)*100
        print 'Total = %d, Correct = %d, Wrong = %d, Accuracy = %.2f' % \
                                                (total, correct, wrong, self.accuracy)        
    #end

    #start writeOutput
    def writeOutput(self, filename, writeOption='w'):
        fp = open(filename, writeOption)
        for i in self.results:
            res = self.results[i]
            for j in res:
                item = res[j]
                text = item['text'].strip()
                label = item['label']
                writeStr = text+" | "+label+"\n"
                fp.write(writeStr)
            #end inner loop
        #end outer loop      
    #end writeOutput    
    
    #start getHTML
    def getHTML(self):
        return self.html.getResultHTML(self.keyword, self.results, self.time, self.pos_count, \
                                       self.neg_count, self.neut_count, 'naivebayes')
    #end
#end class

# load the configurations
'''
try:
    config = loadConfig()
    algorithm = config.get('algorithm_to_test')
    training_data = config.get('training_data')
    tweets_data = config.get('tweets_data')
    classifier = config.get('classifier')
#   classifier = "hdfs://futuresystems/tmp/input/naivebayes_model.pickle"
    time_period = config.get('time_period')
    keyword = sys.argv[1]
    training_required = config.get('training_required')
except:
'''
training_data = "data/training_data.csv"
tweets_data = "data/tweets_data.csv"
classifier = "naivebayes_model.pickle"
#   classifier = "hdfs://futuresystems/tmp/input/naivebayes_model.pickle"
time_period = "daily"
keyword = sys.argv[1]
training_required = 0

# load the tweets data
tweets = []
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    tweets.append(line)

# instantiate the instance of classifier class
nb = NaiveBayesClassifier(tweets, keyword, time_period, training_data, classifier, training_required)
# run the classifier model on tweets
nb.classify()


'''
# load the stopwords list
stopWords = getStopWordList('data/feature_list/stopwords.txt')

# fetch tweet records from the database
connection = happybase.Connection('somehost')
table = connection.table('mytable')
rows = table.rows(['row-key-1', 'row-key-2'])

# function to clean and pre-process tweets
def processTweet(tweet):

    # convert to lower case
    tweet = tweet.lower()
    # convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    # convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)    
    # remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    # replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    # trim
    tweet = tweet.strip('\'"')
    return tweet

# end

# read stopwords from local file
def getStopWordList(stopWordListFileName):

    stopWords = []
    stopWords.append('AT_USER')
    stopWords.append('URL')

    fp = open(stopWordListFileName, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    return stopWords

# end

# start getfeatureVector
def getFeatureVector(tweet, stopWords):
    featureVector = []  
    words = tweet.split()
    for w in words:
        #replace two or more with two occurrences 
        w = replaceTwoOrMore(w) 
        #strip punctuation
        w = w.strip('\'"?,.')
        #check if it consists of only words
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*[a-zA-Z]+[a-zA-Z0-9]*$", w)
        #ignore if it is a stopWord
        if(w in stopWords or val is None):
            continue
        else:
            featureVector.append(w.lower())
    return featureVector    
#end

#start extract_features
def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in featureList:
        features['contains(%s)' % word] = (word in tweet_words)
    return features
#end

# process the records one by one
count = 0;
featureList = []
tweets = []
for key, data in rows:
#    sentiment = data[0]
    tweet = data[1]
    processedTweet = processTweet(tweet)
    featureVector = getFeatureVector(processedTweet, stopWords)
    featureList.extend(featureVector)
    tweets.append((featureVector, sentiment));
#end loop
'''
