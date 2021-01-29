# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 20:56:03 2021

@author: gusta
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, plot_confusion_matrix
from sklearn import preprocessing

# This is a merge of a variety of datasets on treaty ratification for the
# 9 UN human rights treaties,
# It has days from opening of treaty to ratification counted and
# a binary for ratified / not ratified,
# as wel as exogenous variables on mean HDI score, mean GDP, years of uninterrumpted
# democracy at 2015 and religion.
# The data wrangling is not perfect. Since state names change (ie. Venezuela
# vs Bolivarian Republic of Venezuela, etc.) the merge operation 
# ended up dropping observations, but it is sufficient to start doing some tests

df = pd.read_csv('C:/Users/gusta/Documents/Datasets/9t/df_simple.csv')

df.head()
df.info()
df.columns

# I need to encode religion as a numerical for sklearn / numpy. 

le = preprocessing.LabelEncoder()
le.fit(df['Main.religion'])
df['rel'] = le.transform(df['Main.religion'])

# Let's try to predict ICCPR ratifications with our exogenous variables:
# mean hdi, mean gdp, years of democracy and religion. Here we designate
# the "target", and the "features". We have to turn them into np arrays
# for sklearn
y = df['bin_ICCPR'].values
X = df[['hdi_m', 'gdp_m','span_y', 'rel']].values

# The train test split which allows us to test out of sample predictive power
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.3, random_state=25)

# first we set up a knn classifier to predict the binary outcome
# in light of the exog variables.

clf1 = KNeighborsClassifier(n_neighbors=3).fit(X_train,y_train)

# Here we make out of sample predictions and get the predicion score
y_pred = clf1.predict(X_test)
print(y_pred[0:21])
print(clf1.score(X_test, y_test))

# we get cross nine-fold validation scores and plot them.
cv_scores1 = cross_val_score(clf1,X_test,y_test,cv=9)
print(cv_scores1)
fig, ax = plt.subplots()
ax.plot(cv_scores1)
ax.hlines(y=np.mean(cv_scores1),xmin=0,xmax=8, color = 'red')
print("Average 5-Fold CV Score: {}".format(np.mean(cv_scores1)))

# As well as the confusion matrix which will tell us about the correct and
# incorrect classification and types of error.
print(confusion_matrix(y_test,y_pred))
plot_confusion_matrix(clf1, X_test,y_test)

# Now lets try a decision tree model
clf3 = DecisionTreeClassifier().fit(X_train,y_train)
y_pred = clf3.predict(X_test)
print(y_pred[0:21])
print(clf3.score(X_test, y_test))


# Cross validation for out of sample prediction
cv_scores3 = cross_val_score(clf3,X_test,y_test,cv=9)
print(cv_scores3)
fig, ax = plt.subplots()
ax.plot(cv_scores3)
ax.hlines(y=np.mean(cv_scores3),xmin=0,xmax=8, color = 'red')
print("Average 5-Fold CV Score: {}".format(np.mean(cv_scores3)))


# Confusion matrix
print(confusion_matrix(y_test,y_pred))
plot_confusion_matrix(clf3, X_test,y_test)

#fig, ax = plt.subplots()
#ax = plot_tree(clf3,filled=True)

# I could get the feature importances from the tree model (not from the knn one?)
# This might be the most important info. HDI and GDP are the most important
# predictor of ratification. I think there is a way to get pvalues from tree 
# models.   
clf3.feature_importances_

# Let's plot the tree. I had to struggle to find a way to make the image
# readable. Plot below can be recycled.

fig, ax = plt.subplots(figsize=(100, 100))
plot_tree(clf3, filled=True, ax=ax)
plt.show()

fig.savefig('tree.png',format='png')
