import os, sys, json, pickle, happybase, logging, datetime
from functions import *
import methods
#import config
import get_twitter_data
from naive_bayes_classifier import NaiveBayesClassifier


# set the log file
#logging.basicConfig(filename='logs.log',level=logging.DEBUG)
#log('Main process started')


# load the configurations
try:
	config = loadConfig()
	algorithm = config.get('algorithm_to_test')
	training_data = config.get('training_data')
	tweets_data = config.get('tweets_data')
	classifier = config.get('classifier')
	time_period = config.get('time_period')
	keywords = config.get('keywords')
	training_required = config.get('training_required')
except:
	training_data = "./data/training_data.csv"
	tweets_data = "./data/tweets_data.csv"
	classifier = "./input/naivebayes_model.pickle"
	time_period = "daily"
	keywords = "hillary-trump"
	training_required = 0
#	log('Failed to load configurations; error in function loadConfig; exiting...', 'error')
#	print 'FAILED to load configurations'


# check if the model dump file is missing
#if training_required == 0:
#	if not os.path.exists(classifier):
#		training_required = 1

# train a model if required
if training_required:
	tweets = []
	nb = NaiveBayesClassifier(tweets, keywords, time_period, training_data, classifier, training_required)

# create the HBase tweets table if missing
print "Checking database tables..."
try:
	connection = happybase.Connection('localhost')
	connection.create_table('tweets',
		{'keyword': dict(max_versions=10),
		'sentiment': dict(max_versions=10),
		'tweet': dict(max_versions=10)
		}
	)
	print "...OK"
except:
	print "Table already exists"
#	log('Table already exists; skipping creation.')


# check if tweets data files are missing
if not os.path.exists('./input/hillary.txt'):
	dir = os.path.realpath('..')
	keyword = 'hillary'
	trainingDataFile = '/home/cc/twitterSentiment/src/input/hillary.txt'
	inpfile = open(trainingDataFile, "r")
	lines = inpfile.read().split()
	tweets = []
	for tweet in tweets:
		tweets.append(tweet)
	time = 'daily'
	classifierDumpFile = '/home/cc/twitterSentiment/src//input/naivebayes_model.pickle'
	trainingRequired = 0
	# instantiate the instance of classifier class
	nb = NaiveBayesClassifier(tweets, keyword, time, \
								  trainingDataFile, classifierDumpFile, trainingRequired)
	# run the classifier model on tweets
	nb.classify()
	htmlcode = nb.getHTML()
	htmlfile = open('/var/www/html/index.html','w')
	htmlfile.write(htmlcode)
	htmlfile.close()
#	time = 'lastweek'
#	twitterData = get_twitter_data.TwitterData()
#	tweets = twitterData.getTwitterData(keyword, time)

if not os.path.exists('./input/trump.txt'):
	keyword = 'trump'
#	time = 'lastweek'
#	twitterData = get_twitter_data.TwitterData()
#	tweets = twitterData.getTwitterData(keyword, time)



'''
# train a model if data loading successful
if loadSuccess:
	log('Data loading completed successfully')
	try:
		trainingSuccess = methods.trainModel(algorithm)
	except:
		log('Failed to train the model; error in function trainModel; exiting...', 'error')
		print 'FAILED to train the model'
		sys.exit()
else:
	log('Failed to load the data in HBase; error in function loadData; exiting...', 'error')
	sys.exit()

	
# run the model on test data if model successfully trained
if trainingSuccess:
	log('Model trained successfully')
	try:
		testSuccess = methods.testModel(algorithm)
	except:
		log('Failed to run the model on test data; error in function testModel; exiting...', 'error')
		print 'FAILED to run the model'
		sys.exit()
else:
	log('Failed to train the model; error in function trainModel; exiting...', 'error')
	print 'FAILED to train the model'
	sys.exit()


# visualize the result if analysis completed successfully
if testSuccess:
	log('Model run on test data successfully')
	try:
		visualizeSuccess = methods.visualizeResults()
	except:
		log('Failed to visualize the results; error in function visualizeResults; exiting...','error')
		print 'FAILED to visualize the results'
		sys.exit()	
else:
	log('Failed to run the model on test data; error in function testModel; exiting...','error')
	print 'FAILED to run sentiment analysis'
	sys.exit()


# show error message if visualization failed
if visualizeSuccess:
	log('Visualization completed successfully')
	print 'Analysis completed successfully'
else:
	log('Failed to visualize the results; error in function visualizeResults; exiting...','error')
	print 'FAILED to visualize the results'
	sys.exit()
# end of comment block
'''
# end of file
