# MIT-Course-6.0001-Assignment-Problem Set 5

### 5 - Monitor news feeds over the internet 

### Goal: 
filter the news, alerting the user when it notices a news story that matches that user's interests 

#### Knowledge: 
1. use object-oriented programming - classes and inheritance 

#### Challenges:
1. for each problem, lines of code under 15-20 lines
2. understanding abstract class

#### Learning Notes:
1. Data Structure design
2. Class concept and class method debugging
3. Class - subclass - what attributes to put in __init__
4. consider every situation - issues have caused by: not considering to put phrase to lower case; punctuation exceptions purple@#$%cow not considered
5. how to set up timezone on datetime

#### To Solve - solved
1. unsolved: Polling...object has no attribute 'description'
-> mainly due to the old implementation of feedparser.py. 
-> use their new version and updated the code 

#### Possible Further Development:
1. Live auto feedparser - auto run feedparser that can push the user daily news that has met user's requirements
2. Semantic analysis on the news