import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle

with open('X_data.pkl', 'rb') as f:
    X = pickle.load(f)

X = X.drop(columns=["Title", "Year", "Rated", "Released", "Genre", "Director", "Writer", "Actors",\
                    "Plot", "Language", "Country", "Awards", "Metascore", "imdbRating", "imdbVotes",\
                    "tconst", "BoxOffice", "RottenTomatoes", "Production budget", "nconst",\
                    "adjusted_box_office", "log_profit", "NaN"])

X = X.dropna()

y = X["profit"]
X = X.drop(columns="profit")
y = (y > 1) * 1
y = y.astype("category")


# NOTE: Make sure that the outcome column is labeled 'target' in the data file
training_features, testing_features, training_target, testing_target = \
            train_test_split(X, y, random_state=None)

# Average CV score on the training set was: 0.8398983481575604
pipeline = RandomForestClassifier(bootstrap=True, criterion="gini", max_features=0.4, min_samples_leaf=1, min_samples_split=4, n_estimators=100)

pipeline.fit(training_features, training_target)

def predict_profit(x):
    return pipeline.predict(x)

#y_pred = pipeline.predict(testing_features)
#print('accuracy', accuracy_score(testing_target, y_pred))

