# -*- coding: utf-8 -*-
"""Data Breach.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1JlM1p1Fnp8J_J7QzzloZw1z4dnNOT3Nb

<h1>Study on Data Breach Detection using Natural Language Processing and Machine Learning Methods</h1>
<h3> Dinesh Kumar . C</h3>
<h3> 23MCA0173</h3>
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
import nltk
from nltk.tokenize import RegexpTokenizer
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import GradientBoostingClassifier
import seaborn as sns

# numpy, pandas: Libraries for handling data and performing calculations.
# matplotlib.pyplot: For creating visualizations.
# scikit-learn: Used for machine learning algorithms like Naive Bayes, Random Forest, etc.
# nltk: Natural Language Toolkit for text processing.
# seaborn: A library for statistical data visualization.

"""## 1) Exploratory Data Analysis"""

df = pd.read_csv('Original Dataset.csv')
df.head()

# Print the header and count of data points
print("Header (Column Names):")
print(df.columns)
print("\nNumber of data points:")
print(len(df))
target_column = 'Story'
# Print the count of target labels
print(f"\nTarget labels '{target_column}':")

"""### 1.1) Frequency of various type of Data Breach"""

fig = plt.figure(figsize=(20,6))
df.groupby('Method of Leak').Story.count().plot.bar(ylim=0)
plt.show()

# groupby('Method of Leak'): Groups the dataset by the "Method of Leak" column.
# Story.count(): Counts the number of stories per method of leak.
# plot.bar(): Displays a bar chart of these counts.

"""### 1.2) Number of Data Breach Incidents in Various Sectors"""

fig = plt.figure(figsize=(20,4))
df.groupby('Sector').Story.count().plot.bar(ylim=0)
plt.show()

"""### 1.3) Number Of Incidents Per Year"""

fig = plt.figure(figsize=(8,6))
df.groupby('Year').count().plot.bar(ylim=0)
plt.show()

"""### 1.4) Number of Records Lost Per Year"""

fig = plt.figure(figsize=(22,6))
dfplt = pd.DataFrame()
dfplot = df.groupby('Year')['Records_Lost'].sum()
dh = dfplot.to_frame()
plt.plot(dh['Records_Lost'])

"""## 2) Text analysis on Story of DataBreaches"""

import re #Imports the regular expressions library for pattern matching and string manipulation.
from wordcloud import WordCloud, STOPWORDS #Imports WordCloud to generate a word cloud, and STOPWORDS to remove common words like "and" or "the".
import networkx as nx #Imports NetworkX for creating and analyzing network graphs.
import nltk #Imports the Natural Language Toolkit (NLTK) for text processing.
from nltk.corpus import stopwords #Imports stop words from NLTK to remove common words from text analysis.
import itertools #Imports itertools for creating efficient iterators, useful in text processing and bigram generation.
import collections #Imports the collections module for counting and grouping items (e.g., words).
from nltk import bigrams #Imports the bigrams function to generate pairs of consecutive words from a text.
from nltk.tokenize import RegexpTokenizer #Imports RegexpTokenizer for splitting text into words based on a regular expression pattern.
from sklearn.feature_extraction.text import TfidfVectorizer #Imports the TfidfVectorizer to transform text into TF-IDF feature vectors.
from nltk.stem import WordNetLemmatizer #Imports WordNetLemmatizer to reduce words to their base or root form (lemmatization).
from sklearn.cluster import KMeans #Imports KMeans algorithm for clustering similar data points in unsupervised learning.
from nltk.sentiment.vader import SentimentIntensityAnalyzer #Imports VADER for sentiment analysis of text.
from nltk.sentiment.util import * #Imports utilities for sentiment analysis from the NLTK sentiment module.
from textblob import TextBlob #Imports TextBlob for performing various text-processing tasks, such as sentiment analysis and language translation.
from bs4 import BeautifulSoup #Imports BeautifulSoup for parsing and extracting data from HTML or XML documents.

"""### 2.1) Getting the text for analysis"""

df['Story']
dword = df['Story'].dropna()
dword

# Creates a new variable dword that contains the 'Story' column with any missing (NaN) values removed, ensuring that only valid, non-empty text entries are kept for analysis.

"""### 2.2) Cleaning the text data"""

!pip install nltk
# Natural Language Toolkit (NLTK) library in Python.
# NLTK is a popular library for working with human language data (text) and is widely used for tasks related to natural language processing (NLP).

import nltk
nltk.download('stopwords')

#"Stopwords" are common words (like "and," "the," "is," etc.) that are often removed from text during natural language processing (NLP) tasks because they don't carry significant meaning.

def clean(x):
    x = BeautifulSoup(x).get_text()  # Remove HTML tags
    x = re.sub('[^a-zA-Z]', ' ', x)  # Remove non-letter characters
    x = x.lower().split()  # Convert to lowercase and split into words
    stop = set(stopwords.words('english'))  # Load stop words
    words = [w for w in x if not w in stop]  # Remove stop words
    return(' '.join(words))  # Join words into a single string
dword = dword.apply(lambda x: clean(x))

display(dword.head(10))

"""### 2.3) Finding the words in the data and removing stopwords

"""

words_in_story = [story.lower().split() for story in dword]
words_in_story[0]

stop_words = set(stopwords.words('english'))
list(stop_words)[0:10]

story_nsw = [[word for word in story_words if not word in stop_words]
              for story_words in words_in_story]
story_nsw[0]

""" 2.4) Storing the count of words and finding most common words"""

all_words_nsw = list(itertools.chain(*story_nsw)) #Flattens the list of lists story_nsw (which contains words from each story) into a single list of all words. itertools.chain(*story_nsw) combines all inner lists into one continuous sequence, and list() converts it back into a Python list.
counts_nsw = collections.Counter(all_words_nsw)
counts_nsw.most_common(15)

"""### 2.5) Plotting the common terms

<!-- 1.   List item
2.   List item -->


"""

clean_story_nsw = pd.DataFrame(counts_nsw.most_common(15),
                             columns=['words', 'count'])
fig, ax = plt.subplots(figsize=(8, 8))
# Plot horizontal bar graph
clean_story_nsw.sort_values(by='count').plot.barh(x='words',
                      y='count',
                      ax=ax,
                      color="orange")
ax.set_title("Common Terms Found in Story (Without Stop Words)")
plt.show()

"""### 2.6) Exploring some co-occuring terms using bi-grams"""

terms_bigram = [list(bigrams(term)) for term in story_nsw]
terms_bigram[0]

# Bigrams refer to pairs of consecutive words that appear together in a given text. They are a simple form of n-grams, where "n" represents the number of words grouped together

"""### 2.7) Counting and display top 30 common bi-grams"""

# Flatten list of bigrams in clean story
bigrams = list(itertools.chain(*terms_bigram))
# Create counter of words in clean bigrams
bigram_counts = collections.Counter(bigrams)
bigram_counts.most_common(30)

bigram_df = pd.DataFrame(bigram_counts.most_common(20),
                             columns=['bigram', 'count'])
bigram_df

"""#### 2.8) Visualizing network of bi-grams"""

d = bigram_df.set_index('bigram').T.to_dict('records')
G = nx.Graph()
# Create connections between nodes
for k, v in d[0].items():
    G.add_edge(k[0], k[1], weight=(v * 3))
fig, ax = plt.subplots(figsize=(12, 10))
pos = nx.spring_layout(G, k=4)
# Plot networks
nx.draw_networkx(G, pos,
                 font_size=10,
                 width=2,
                 edge_color='grey',
                 node_color='green',
#                edge_length = 10,
                 with_labels = False,
                 ax=ax)
# Create offset labels
for key, value in pos.items():
    x, y = value[0]+.00167, value[1]+.045
    ax.text(x, y,
            s=key,
            bbox=dict(facecolor='blue', alpha=0.4),
            horizontalalignment='center', fontsize=10)
plt.show()

# Network diagrams (also called Graphs) show interconnections between a set of entities. Each entity is represented by a Node (or vertice). Connections between nodes are represented through links (or edges).

"""### 3) Sentimental Analysis on DataBreach Story Data"""

import nltk
nltk.download('vader_lexicon')
#VADER (Valence Aware Dictionary and sEntiment Reasoner) is a lexicon and rule-based sentiment analysis tool specifically designed to analyze the sentiment of textual data.

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.util import *
from nltk.corpus import stopwords
from nltk import tokenize
sentiment = pd.DataFrame()
sid = SentimentIntensityAnalyzer()

sentiment['sentiment_compound_polarity']=dword.apply(lambda x:sid.polarity_scores(x)['compound'])
sentiment['sentiment_neutral']=dword.apply(lambda x:sid.polarity_scores(x)['neu'])
sentiment['sentiment_negative']=dword.apply(lambda x:sid.polarity_scores(x)['neg'])
sentiment['sentiment_pos']=dword.apply(lambda x:sid.polarity_scores(x)['pos'])
sentiment['sentiment_type']=''
sentiment.loc[sentiment.sentiment_compound_polarity>0,'sentiment_type']='Positive'
sentiment.loc[sentiment.sentiment_compound_polarity==0,'sentiment_type']='Neutral'
sentiment.loc[sentiment.sentiment_compound_polarity<0,'sentiment_type']='Negative'
sentiment.head(3)

sentiment.sentiment_type.value_counts()

colors = ['blue', 'yellow', 'red']
explode = (0, 0.08, 0.1)
sentiment.sentiment_type.value_counts().plot(kind='pie', figsize=(9, 7), title="Sentiment Analysis of Data Breach Stories (Pie Graph)", colors=colors, explode=explode,autopct='%1.1f%%', shadow=False)

"""### We can clearly see that negative stories are more as it is all about data breach

---


"""





"""## 4) Machine Learning Techniques to predict method of Data Breach

### 4.1)Preprocessing of Data

**4.1.1) counting categories of data**
"""

df['Method of Leak'].value_counts()

list(df.columns.values)

dfmodel = pd.DataFrame()
dfmodel['Story'] = df['Story']
dfmodel['Method of Leak'] = df['Method of Leak']
dfmodel

dfmodel = dfmodel.dropna()
dfmodel.head()

dfmodel['Method of Leak'].value_counts()

"""**4.1.2) We will be picking only top five category for our machine learning model as other categories have less observations and we will remove rows containing NaN**"""

dfmodel["label"] = dfmodel['Method of Leak'].map({'Hacked':0,
'Lost / stolen device or media':1,
'Inside job ' : 2,
'Accidentally published' : 3,
'Poor security' : 4,
'Inside job' : 5 })

dfmodel = dfmodel.dropna()
dfmodel

"""**4.1.3) We will tokenize our story input and count the terms using text data preprocessing methods**"""

from nltk.tokenize import RegexpTokenizer

token = RegexpTokenizer(r'[a-zA-Z0-9]+')
cv = CountVectorizer(lowercase=True,stop_words='english',ngram_range = (1,1),tokenizer = token.tokenize)
text_counts= cv.fit_transform(dfmodel['Story'])

"""### 4.2) Creating the testing and training dataset , here X is the input story and y is the method of Leak"""

num_samples = text_counts.shape[0]
num_features = text_counts.shape[1]

print(f"Number of samples: {num_samples}")
print(f"Number of features: {num_features}")

X_train, X_test, y_train, y_test = train_test_split(text_counts, dfmodel['label'], test_size=0.1,shuffle=True, random_state=105)

"""### 4.3) Applying Multinomial Naive Bayes classifier model for Prediction"""

model1 = MultinomialNB().fit(X_train, y_train)
md1predicted= model1.predict(X_test)

print("MultinomialNB Accuracy:",metrics.accuracy_score(y_test, md1predicted))

print("confusion_matrix",confusion_matrix(y_test,md1predicted))

conf_mat = confusion_matrix(y_test,md1predicted)
ax = sns.heatmap(conf_mat, annot=True, fmt="d")

print("classification_report")
print(classification_report(y_test,md1predicted))

"""### 4.4) Applying Random Forest Model for Prediction"""

model2 = RandomForestClassifier(n_estimators=1000, random_state=0)
model2.fit(X_train, y_train)

md2predicted = model2.predict(X_test)

print("Random Forest Accuracy",metrics.accuracy_score(y_test, md2predicted))

print("confusion_matrix",confusion_matrix(y_test,md2predicted))

conf_mat = confusion_matrix(y_test,md2predicted)
ax = sns.heatmap(conf_mat, annot=True, fmt="d")

print("classification_report")
print(classification_report(y_test,md2predicted))

"""### 4.5) Applying Stochastic Gradient Descent model for prediction"""

model3 = SGDClassifier().fit(X_train, y_train)
model3.fit(X_train, y_train)

md3predicted = model3.predict(X_test)

print("SGD Accuracy",metrics.accuracy_score(y_test, md3predicted))

print("confusion_matrix")
print(confusion_matrix(y_test,md3predicted))

conf_mat = confusion_matrix(y_test,md3predicted)
ax = sns.heatmap(conf_mat, annot=True, fmt="d")

print("classification_report")
print(classification_report(y_test,md3predicted))

"""### 4.6) Applying Gradient Boosting Classifier Model for Prediction"""

model4 = GradientBoostingClassifier().fit(X_train, y_train)
model4.fit(X_train, y_train)

md4predicted = model4.predict(X_test)

print("Gradient Boosting Classifier Accuracy",metrics.accuracy_score(y_test, md4predicted))

print("confusion_matrix")
print(confusion_matrix(y_test,md4predicted))

conf_mat = confusion_matrix(y_test,md4predicted)
ax = sns.heatmap(conf_mat, annot=True, fmt="d")

print("classification_report")
print(classification_report(y_test,md4predicted))

"""### 4.7) Which Model is The Best"""

model_name = ['MNB','RandomForest','SGD','GradientBoosting']

accuracy = [metrics.accuracy_score(y_test, md1predicted),metrics.accuracy_score(y_test, md2predicted),
\metrics.accuracy_score(y_test, md3predicted),metrics.accuracy_score(y_test, md4predicted)]

accuracy

import seaborn as sns
import matplotlib.pyplot as plt
sns.boxplot(x=model_name, y=accuracy)
plt.xlabel('Model')
plt.ylabel('Accuracy')
plt.title('Accuracy Comparison')
plt.show()