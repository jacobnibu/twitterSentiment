import naive_bayes_classifier, classifier_helper, nltk
import json, logging, html_helper
from classifier_helper import *
'''
trainingDataFile = 'data/training_sample.csv'
inpfile = open(trainingDataFile, "r")
line = inpfile.readline()
count = 1
tweetItems = []
opinions = []
while line:    
    count += 1
    splitArr = line.split('|')
    processed_tweet = splitArr[0].strip()
    try:
		opinion = splitArr[1].strip()
    except:
		opinion = 'neutral'
    if(opinion != 'neutral' and opinion != 'negative' and opinion != 'positive'):
        opinion = 'neutral'
		#print('Error with tweet = %s, Line = %s') % (processed_tweet, count)
    tweet_item = processed_tweet, opinion
    tweetItems.append(tweet_item)    
    line = inpfile.readline()
#end while loop

tweets = []    
for (words, sentiment) in tweetItems:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    tweets.append((words_filtered, sentiment))

helper = classifier_helper.ClassifierHelper('data/feature_list.txt')
training_set = nltk.classify.apply_features(helper.extract_features, tweets)
classifier = nltk.NaiveBayesClassifier.train(training_set)
print nltk.classify.accuracy(classifier, training_set)
#classifier.show_most_informative_features(10)
'''
trainingDataFile = 'data/sampleTweets.csv'
inpfile = open(trainingDataFile, "r")
lines = inpfile.read().split()
tweets = []
for tweet in tweets:
    tweets.append(tweet)
keyword = 'hillary'
time = 'daily'
classifierDumpFile = 'data/naivebayes_model.pickle'
trainingRequired = 0
# instantiate the instance of classifier class
nb = naive_bayes_classifier.NaiveBayesClassifier(tweets, keyword, time, \
							  trainingDataFile, classifierDumpFile, trainingRequired)
# run the classifier model on tweets
nb.classify()
nb.getHTML()
