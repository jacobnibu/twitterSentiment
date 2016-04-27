import os, happybase
# load if file exists in current directory
if os.path.exists('data/stopwords.txt'):
	try:
		f = open('data/stopwords.txt', 'r')
		stopwords = f.readlines()
		f.close()
	except:
		print 'Could not open the stopwords file for reading'

	try:
		connection = happybase.Connection('localhost')
	except:
		print 'Could not get connection object'

	try:
		connection.create_table(
				'stopwords',
				{'cf1': dict(max_versions=10)
#				 'cf2': dict(max_versions=1, block_cache_enabled=False),
#				 'cf3': dict(),  # use defaults
				}
			)
	except:
		print 'Could not create table stopwords'
	
	table = connection.table('stopwords')

	try:
		for index, stopword in enumerate(stopwords):
			index += 1
			table.put(str(index),{'cf1:': stopword})
	except:
		print 'Could not put stopwords in stopwords table'

else:
	print 'Stopwords data file not found'
