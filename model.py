import numpy as np
from sklearn.model_selection import *
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import *
import json
from sklearn.metrics import *

np.random.seed(2) #for reproducibility



class Modeller(object):
	
	def __init__(self, x_tr = None, x_test = None, y_tr = None, y_test = None):
		self.X_train, self.X_test, self.y_train, self.y_test = x_tr, x_test, y_tr, y_test

	def clean(self):
		#read from file
		X = np.genfromtxt('<dataset>', delimiter=',',dtype=None)
		
		#preprocess
		
		X = X[1:,:] #remove column headings
		y = X[:,24] #getting labels
		X = X[:,:24] #remove labels for training

		#separate into train and test set by random sampling
		self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2)


	def other_models(self):
		'''
		This method tests various models on the dataset. We found
		RandomForest to perform the best, so we are using that as
		the final model.
		'''
		
		self.clean()
		
		#trying out decision tree classifier(approx 73%)
		clf = DecisionTreeClassifier()
		clf.fit(self.X_train, self.y_train)
		
		y_pred = clf.predict(self.X_test)
		print('Accuracy for DT:', accuracy_score(y_pred, self.y_test))
		
		scores = cross_val_score(clf, self.X_test, self.y_test, cv=5)
		print('5 fold CV score for DT:',scores.mean())

		#82.49%
		clf = KNeighborsClassifier(n_neighbors = 6)
		clf.fit(self.X_train, self.y_train)
		
		y_pred = clf.predict(self.X_test)
		print('Accuracy for KNN:', accuracy_score(y_pred, self.y_test))
		
		scores = cross_val_score(clf, self.X_test, self.y_test, cv=5)
		print('5 fold CV score for KNN:',scores.mean())
		
		
		#82.4%
		clf = ExtraTreesClassifier(n_estimators=10)
		clf.fit(self.X_train, self.y_train)
		y_pred = clf.predict(self.X_test)
		print('Accuracy for Extra Trees Classifier:', accuracy_score(y_pred, self.y_test))
		
		scores = cross_val_score(clf, self.X_test, self.y_test, cv=5)
		print('5 fold CV score for Extra Trees:', scores.mean())

	def predict(self, json_ob):
		'''
		Receives a JSON object, parses it into a vector of features and 
		applies RandomForest Classifier on it. It returns a JSON object
		of the form id:probability of dropping out.
		'''
		self.clean()
		
		#creating a classifier. 10 turned out to be the best value for number of estimators
		
		clf = RandomForestClassifier(n_estimators=10)
		
		#first we train
		clf.fit(self.X_train, self.y_train)
		
		#JSON parsing
		parsed_json = json.loads(json_ob)
		
		res = dict()

		for key in parsed_json.keys():
			list_feat = parsed_json[key]['feat']
			np_feat = np.asarray(list_feat).reshape((1,24))
			res[key] = str(clf.predict_proba(np_feat)[0][1])

		return json.dumps(res)

'''
m = Modeller()
m.other_models()
'''
#uncomment to see performance on all models
