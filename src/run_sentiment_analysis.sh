#!/bin/bash

echo "==================================="
echo "Starting Twitter Sentiment Analyzer"
echo "==================================="

# export the environment variables
echo "setting the environment variables"
export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64
export HADOOP_HOME=/opt/hadoop
export PATH=$JAVA_HOME/bin:$HADOOP_HOME/bin:/opt/hbase/bin:$PATH

# start thrift server
echo "starting HBase Thrift server..."
#hbase thrift start >/dev/null 2>&1
hbase thrift start >/dev/null 2>&1 &
sleep 5
echo "Thrift server running"


# clean up any files from previous runs
echo "removing previously built files and directories"
echo "-----------------------------------------------"
#hdfs dfs -rm -r hdfs://futuresystems/tmp/input
#hdfs dfs -rm -r hdfs://futuresystems/tmp/output*
#hdfs dfs -rm -r hdfs://futuresystems/tmp/src
echo "-----------------------------------------------"

# copy data files to hdfs; only files for hadoop; from local input directory
#echo "copying data files to HDFS"
#hdfs dfs -mkdir /tmp/input
#hdfs dfs -mkdir /tmp/src
#hdfs dfs -mkdir ~/input
#hdfs dfs -put /home/cc/sw-project-template/data/input/* /tmp/input
#hdfs dfs -put /home/cc/sw-project-template/src/* /tmp/src

# make the mapper executable
#echo "preparing the python files ready for hadoop"
#chmod +x /home/cc/sw-project-template/src/sentiment_mapper.py

# train the model and get ready to run the model on test data
echo "======================================"
echo "Starting to train the classifier model"
echo "======================================"
python /home/cc/sw-project-template/src/main.py
#python /home/cc/sw-project-template/src/main.py &
#wait
echo "completed training the model"
sleep 1

# call hadoop to run the model on test
echo "starting to run the model on tweets related to Hillary"
echo "First iteration of Hadoop process"
trainingDataFile = '../data/input/hillary.txt'
inpfile = open(trainingDataFile, "r")
lines = inpfile.read().split()
tweets = []
for tweet in tweets:
    tweets.append(tweet)
keyword = 'hillary'
time = 'daily'
classifierDumpFile = '../data/input/naivebayes_model.pickle'
trainingRequired = 0
# instantiate the instance of classifier class
nb = naive_bayes_classifier.NaiveBayesClassifier(tweets, keyword, time, \
							  trainingDataFile, classifierDumpFile, trainingRequired)
# run the classifier model on tweets
nb.classify()
nb.getHTML()
#hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar -D mapred.reduce.tasks=1 -file /home/cc/sw-project-template/src/sentiment_mapper.py -mapper "sentiment_mapper.py hillary" -file /home/cc/sw-project-template/src/sentiment_reducer.py -reducer "sentiment_reducer.py" -input /tmp/input/hillary.txt -output /tmp/output_hillary -file /home/cc/sw-project-template/data/input/feature_list.txt -file /home/cc/sw-project-template/data/input/naivebayes_model.pickle
echo "Completed the first iteration of hadoop"
echo "=========================>>>>>><<<<<<<========================"
sleep 1
echo "starting to run the model on tweets related to Trump"
echo "Second iteration of Hadoop process"
#hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar -D mapred.reduce.tasks=0 -file /home/cc/sw-project-template/src/sentiment_mapper.py -mapper '/home/cc/sw-project-template/src/sentiment_mapper.py trump' -input hdfs://futuresystems/tmp/input/trump.txt -output hdfs://futuresystems/tmp/output_trump
echo "Completed the second iteration of hadoop"
echo "Analysis phase completed"
echo "=========================>>>>>><<<<<<<========================"
sleep 1
# call the visualization process
echo "visualizing the results"
#python /home/cc/sw-project-template/src/visualize_results.py
echo "Twitter Sentiment Analysis completed"
