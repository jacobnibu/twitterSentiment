**Twitter Sentiment Analysis of the 2016 U.S. Presidential Election**
=====================================================================

The purpose of this project is to analyze the public sentiment reflected in Tweets pertaining to the leading US Presidential candidates for 2016 election by using a supervised machine learning algorithm that runs on a Hadoop cluster. The project builds on the existing work of Ravikiran Janardhana by adapting it to run on MapReduce framework and use HBase as the data source rather than a flat file on the local disk. The output data from the analysis will also be stored in HBase and relevant visualizations will be run against the database.

Deployment and scheduling will be done using Ansible playbook. The existing code will be redesigned to utilize parallelism to improve the performance. Training data from the original project will be used to train the model. We envision that one iteration of MapReduce will train the model and a second iteration will run the model on the test data to output the final results.

**Team**
--------

•	Ian Bass, ibass, ibass, ibass (Lead)
•	Nibu Jacob, jacobn, jacobn, jacobn
•	Madhavi Polu, mpolu, mpolu, madhavi

**Role**
^^^^^^^^

•	Deployment: mpolu
•	Configuration: mpolu
•	Database: ibass
•	Map/Reduce Functions: jacobn
•	Algorithm: jacobn
•	Plot: ibass/mpolu (TBD)

**Artifacts**
-------------

•	Statistical Results

**List of Technologies**
------------------------

**Development Languages**
^^^^^^^^^^^^^^^^^^^^^^^^^

•	Python

**Software Tools**
^^^^^^^^^^^^^^^^^^

•	Ansible
•	Hadoop
•	HBase
•	Python

**Compute Resources**
---------------------

•	OpenStack in FutureSystems

**System Requirements**
-----------------------

•	Size: 3-5 VM instances
•	OS: Ubuntu 14.04 LTS
•	Storage: up to 100GB (TBD)

**List of DataSets**
--------------------

•	Twitter API

**Schedule**
------------

•	Week 1: Initial Meeting
•	Week 2: Proposal
•	Week 3: Discussion
•	Week 4: Presentation
•	Week 5: Refine raw dataset
•	Week 6: Build systems
•	Week 7: Develop modules, test run
•	Week 8: Final Report, Review, Submission

**Project Style and Type**
--------------------------

•	Basic
•	Analytics

**Acknowledgement**
-------------------

Sentiment Analysis idea to be built from previous work from the following sources:

•	Ravikiran Janardhana : Twitter Sentiment Analyzer - https://github.com/ravikiranj/twitter-sentiment-analyzer
•	Big Data Stack Repository - https://github.com/futuresystems/big-data-stack