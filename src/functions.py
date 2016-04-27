
# ============================================================================
# function to log the process flow
# ============================================================================

def log(message, level='info'):
	logging.info(str(datetime.datetime.now()))
	if level == 'error':
		logging.error(message)
	else:
		logging.info(message)
	logging.info('-----------------------------------------------------')


# ============================================================================
# function to load configurations
# ============================================================================

def loadConfig():
	config = {}
	# load if file exists in current directory
	if os.path.exists('config.json'):
		with open('config.json') as f:
			config.update(json.load(f))
	else:
		log('Config file not found','error')
	# return the array
	return config

# ============================================================================
# function to get connection objection to HBase database
# ============================================================================

def getDBConnection():
	try:
		connection = happybase.Connection('localhost')
		#log('Connection to database established')
		return connection
	except:
		log('Could not get connection to the database','error')
		#sys.exit()

# ============================================================================
# function to 
# ============================================================================


# ============================================================================
# function to load stopwords into HBase
# ============================================================================

def loadStopwords():
	# load if file exists in current directory
	if os.path.exists('data/stopwords.txt'):
		try:
			f = open('data/stopwords.txt', 'r')
			stopwords = f.read().split()
			f.close()
		except:
			log('Could not open the stopwords file for reading','error')
			return False
		
		connection = getDBConnection()
		try:
			connection.create_table(
					'stopwords',
					{'stopword': dict(max_versions=10)
					}
				)
		except:
			log('Table already exists; skipping creation.')
			return False
		
		table = connection.table('stopwords')

		try:
			for index, stopword in enumerate(stopwords):
				index += 1
				table.put(str(index),{'stopword:': stopword})
		except:
			log('Could not put stopwords in stopwords table','error')
			return False
		return True
	else:
		log('Stopwords data file not found','error')
		return False