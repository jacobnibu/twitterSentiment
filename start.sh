#!/bin/bash

# change persmissions on mapper and reducer files
#chmod +x ~/sw-project-template/src/sentiment_mapper.py
#chmod +x ~/sw-project-template/src/sentiment_reducer.py
sudo chmod 777 -R ~/sw-project-template

# run the actual script as hadoop user
chmod +x ~/sw-project-template/src/run_sentiment_analysis.sh
sudo su hadoop -c ~/sw-project-template/src/run_sentiment_analysis.sh
