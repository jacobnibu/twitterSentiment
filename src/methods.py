

# ============================================================================
# function to load all data
# ============================================================================

def loadData(tweets_data):
	inpfile = open(tweets_data, "r")
	lines = inpfile.read().split()
	tweets = []
	for tweet in tweets:
		tweets.append(tweet)
	inpfile.close()
	return tweets

'''
	# get HBase connection object
	connection = getDBConnection()


	# check and load stopwords data
	try:
		tableStopwords = connection.table('stopwords')
	except:
		log('Could not find table stopwords')
		
	row = tableStopwords.scan(limit=1)
	if row is None:
		try:
			loadSWSuccess = loadStopwords()
			if not loadSWSuccess:
				log('Could not load stopwords; error in function loadStopwords','error')
				return False
			else:
				log('Successfully loaded stopwords data')
		except:
			log('Could not load stopwords; error in function loadStopwords','error')
			return False
	else:
		log('Stopwords data already exists in database; proceeding to check for twitter data...')


	# check and load twitter data
	try:
		tableTweets = connection.table('tweets')
	except:
		log('Could not find table tweets')

	row = tableTweets.scan(limit=1)
	if row is None:
		try:
			get_twitter_data()
		except:
			log('Could not load tweets; error in function get_twitter_data','error')
	else:
		log('Twitter data already exists in database')
'''
# ============================================================================
# function to train a model for the algorithm specified
# ============================================================================

def trainModel(self, algorithm):
	if(algorithm == 'naivebayes'):
		trainingDataFile = 'data/training_dataset.csv'
		classifierDumpFile = 'data/naivebayes_model.pickle'
		if os.path.exists(classifierDumpFile):
			trainingRequired = 0
			log('Training not required; trained model available.')
		else:
			trainingRequired = 1
			log('Starting to train a Naive Bayes Classifier...')

		try:
			nb = NaiveBayesClassifier(tweets, keyword, time,\
									  trainingDataFile, classifierDumpFile, trainingRequired)
			log('Completed training a Naive Bayes Classifier')
		except:
			log('Failed to run naive_bayes classifier over training data','error')

		log('Computing accuracy...')
		nb.accuracy()

# ============================================================================
# function to test a model for the algorithm specified
# ============================================================================

def testModel(self, algorithm):
	if(algorithm == 'naivebayes'):
		trainingDataFile = 'data/full_training_dataset.csv'
		classifierDumpFile = 'data/naivebayes_model.pickle'
		if os.path.exists(classifierDumpFile):
			trainingRequired = 0
			log('Training not required; trained model available.')
		else:
			trainingRequired = 1
			log('Starting to train a Naive Bayes Classifier...')

		nb = naive_bayes_classifier.NaiveBayesClassifier(tweets, keyword, time,\
									  trainingDataFile, classifierDumpFile, trainingRequired)

		log('Computing accuracy...')
		nb.accuracy()

# ============================================================================
# function to visualize the results of the analysis
# ============================================================================
