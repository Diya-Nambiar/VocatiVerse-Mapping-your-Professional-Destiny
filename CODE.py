# -*- coding: utf-8 -*-
"""Vocativerse.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1S4D5UNj0oZFdUNsw6GkKsTDzRgDJZQpf
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string

import nltk
nltk.download('punkt')

data=pd.read_csv('/content/coursera_course_dataset_v3.csv')
data.head()

final_data = data[['Title','Skills']]
final_data.head()

def preprocess_title(title):
    # Tokenization
    tokens = word_tokenize(title)
    # Lowercasing and removing punctuation
    tokens = [word.lower() for word in tokens if word.isalpha()]
    # Stemming
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(word) for word in tokens]
    # Joining tokens back into a string
    preprocessed_title = ' '.join(stemmed_tokens)
    return preprocessed_title

final_data['Title'] = final_data['Title'].apply(preprocess_title)

# TF-IDF Vectorization
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(final_data['Skills'])
y = final_data['Title']

final_data["Skills"].str.len().value_counts()
# final_data.iloc[16,]

final_data['Skills'] = final_data['Skills'].apply(lambda x: 'empty' if len(x) == 0 else x)

final_data["Skills"].str.len().value_counts()

from sklearn.feature_extraction.text import TfidfVectorizer
tfv=TfidfVectorizer()

tfv_matrix=tfv.fit_transform(final_data['Skills'])
tfv_matrix

tfv_matrix.shape

from sklearn.metrics.pairwise import sigmoid_kernel
sig=sigmoid_kernel(tfv_matrix,tfv_matrix)

len(final_data["Title"].unique())

final_data["Title"]

indices = pd.Series(final_data.index,index = final_data["Title"]).drop_duplicates()

indices

def give_recommendation(title,sig=sig):
  idx=indices[title]
  sig_scores=list(enumerate(sig[idx]))
  sig_scores=sorted(sig_scores,key=lambda x:x[1],reverse=True)
  sig_scores=sig_scores[1:11]
  job_indices=[i[0] for i in sig_scores]
  return final_data[['Title','Skills']].iloc[job_indices]

def recommender(title):
  job = final_data[final_data["Title"].str.contains(title)].iloc[0]["Title"]
  return give_recommendation(job)

#final_data[final_data["Title"].str.contains('Cybersecurity')].iloc[0]["Title"]

recommender('data scienc')

# knn
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors

# Load the dataset
data = pd.read_csv('/content/coursera_course_dataset_v2_no_null.csv')

# Extract relevant columns
final_data = data[['Title','Skills']]

# TF-IDF Vectorization
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(final_data['Skills'])

# Compute cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Fit Nearest Neighbors model
knn = NearestNeighbors(metric='cosine', algorithm='brute')
knn.fit(tfidf_matrix)

# Function to recommend jobs based on input title
def recommender(title, k=10):
    title_index = final_data[final_data["Title"].str.contains(title)].index[0]
    distances, indices = knn.kneighbors(tfidf_matrix[title_index], n_neighbors=k+1)
    recommended_indices = indices.flatten()[1:]
    return final_data.iloc[recommended_indices]

recommender('Data Science')

## k means

from sklearn.cluster import KMeans

##
final_data = data[['Title','Skills']]

# TF-IDF Vectorization
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(final_data['Skills'])

# Fit KMeans clustering model
num_clusters = 10  # You can adjust this value based on the dataset
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(tfidf_matrix)

# Assign clusters to each course
final_data['Cluster'] = kmeans.labels_

# Function to recommend jobs based on input title
def recommender(title):
    title_skills = tfidf_vectorizer.transform([final_data.loc[final_data['Title'] == title, 'Skills'].values[0]])
    title_cluster = kmeans.predict(title_skills)[0]
    similar_courses = final_data[final_data['Cluster'] == title_cluster]
    return similar_courses.head(10)

recommender('Data Science')



!pip install requests
!pip install bs4
!pip install html5lib

## import requests
# URL = "https://www.naukri.com/fresher-jobs?src=gnbjobs_homepage_srch"
# r = requests.get(URL)
# #print(r.content)
import requests
from bs4 import BeautifulSoup

URL = "https://www.amazon.in/s?k=phones&i=electronics&crid=2YM7MZFLJUXM1&sprefix=phone%2Celectronics%2C200&ref=nb_sb_noss_1"
r = requests.get(URL)

soup = BeautifulSoup(r.text, 'html.parser')
#print(soup.prettify())

skills=[]
job_titles=[]
skill=soup.find('span',class_="a-size-medium a-color-base a-text-normal")
skills.append(skill)
print(skill)
#for page in pages:

