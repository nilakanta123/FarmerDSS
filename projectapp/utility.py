import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.utils import shuffle
from sklearn.svm import SVC

def adjusting(sc):
	d = sc[0]-sc[1]
	if d < 5:
		dd = sc[1]-5
		sc[0] = sc[0]-dd
		sc[1] = sc[1]-dd
		sc[2] = sc[2]-dd

	if sc[2] < 0:
		sc[0] = sc[0]+ -(sc[2])
		sc[1] = sc[1]+ -(sc[2])
		sc[2] = sc[2]+ -(sc[2])

	return sc

def mrange(n):
	l = []
	for i in range(n):
		l.append(1)
	for j in range(10-n):
		l.append(0)
	return l

def get_am_symptom_list():
	res = {}
	s_list = pd.read_csv("./data/am_info.csv")
	res['age']=[tuple(x) for x in s_list[0:6].values]
	res['general']=[tuple(x) for x in s_list[6:18].values]
	res['skin']=[tuple(x) for x in s_list[18:38].values]
	res['breathing']=[tuple(x) for x in s_list[38:46].values]
	res['digestive']=[tuple(x) for x in s_list[46:53].values]
	res['behavioural']=[tuple(x) for x in s_list[53:66].values]
	res['posture']=[tuple(x) for x in s_list[66:75].values]
	res['structure']=[tuple(x) for x in s_list[75:81].values]
	res['discharge']=[tuple(x) for x in s_list[81:89].values]
	return res

def get_am_input(ll):
	s_list = pd.read_csv("./data/am_info.csv")
	res = []
	for i in s_list['symptoms']:
		if i in ll:
			res.append(1)
		else:
			res.append(0)
	return res

def saveamfeedback(pig_farm_address="", farm_phone_no="", email_address="", animal_no="", date_of_sikness="", symptoms="", score="", disease_by_vet="", satisfaction="", suggestion=""):
	df_feedback = pd.read_csv("./data/am_feedback.csv")
	df_feedback = df_feedback.append({'pig_farm_address': pig_farm_address, 'farm_phone_no':farm_phone_no, 'email_address':email_address,
		'animal_no':animal_no,'date_of_sikness':date_of_sikness,'symptoms':symptoms,'score':score, 'disease_by_vet':disease_by_vet,
		'satisfaction':satisfaction, 'suggestion':suggestion}, ignore_index=True)
	df_feedback.to_csv("./data/am_feedback.csv", index=False)

def am_diseases_predict_engine(ll):
	df = pd.read_csv('./data/am.csv')
	labelEncoder = preprocessing.LabelEncoder()
	if df['Probable_disease'].size > 0:
		labelEncoder.fit(df['Probable_disease'])
	df['Probable_disease']=labelEncoder.transform(df['Probable_disease'])
	X, y = shuffle(df.iloc[:,:-3],df.Probable_disease, random_state=13)
	model_svm = SVC(C=26, gamma=0.01, kernel='rbf', probability=True)
	model_svm.fit(X,y)
	prob_list = model_svm.predict_proba([ll])
	mx = max(prob_list[0])
	mn = min(prob_list[0])
	for index, value in enumerate(prob_list[0]):
		x= (value-mn)*9
		y=(x/(mx-mn))+1
		prob_list[0][index]=y
	score_list = sorted(prob_list[0], reverse=True)
	score_list = np.round(score_list)
	pred = (-model_svm.predict_proba([ll])).argsort()[0]
	return labelEncoder.inverse_transform(pred[:3]), adjusting(score_list[:3])

def am_decision_predict_engine(ll,st):
	df = pd.read_csv('./data/am.csv')
	# df.drop(['Probable_agent'], axis=1, inplace=True)	
	pdle = preprocessing.LabelEncoder()
	pale = preprocessing.LabelEncoder()
	dle = preprocessing.LabelEncoder()
	if df['Probable_disease'].size > 0:
		pdle.fit(df['Probable_disease'])
	if df['Probable_agent'].size > 0:
		pale.fit(df['Probable_agent'])
	if df['Decision'].size > 0:
		dle.fit(df['Decision'])
	df['Probable_disease']=pdle.transform(df['Probable_disease'])
	df['Probable_agent']=pale.transform(df['Probable_agent'])
	df['Decision']=dle.transform(df['Decision'])
	X, y = shuffle(df.iloc[:,:-2],df.Decision, random_state=13)
	model2_svm = SVC(C=26, gamma=0.01, kernel='rbf', probability=True)
	model2_svm.fit(X,y)
	ss = pdle.transform([st])
	ll.extend(ss)
	pred = model2_svm.predict([ll])
	return dle.inverse_transform(pred)[0]


# gg = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# print(am_diseases_predict_engine(gg))