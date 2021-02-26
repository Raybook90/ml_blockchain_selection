from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import pickle


def train_decisiontree():
    df = pd.read_csv("dataset.csv")
    ordinal_dict = {'Low': 1, 'Medium': 2, 'High': 3}
    boolean_dict = {'Yes': 1, 'No': 0}
    dict_type = {'Public': 1, 'Private': 0}

    df['type'] = df['type'].map(dict_type)
    df['turing_complete'] = df['turing_complete'].map(boolean_dict)
    df['smart_contract'] = df['smart_contract'].map(boolean_dict)
    df['platform_transaction_speed'] = df['platform_transaction_speed'].map(ordinal_dict)
    df['popularity'] = df['popularity'].map(ordinal_dict)

    X = df.drop('blockchain', axis=1)
    y = df['blockchain']

    le = LabelEncoder()
    y = le.fit_transform(y)

    #Serialize LabelEncoder with pickle
    #pickle.dump(le, open('label_encoder.obj', 'wb'))

    #Serialize LabelEncoder with joblib
    joblib.dump(le, 'label_encoder.joblib')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    dt = DecisionTreeClassifier().fit(X_train, y_train)
    predictions = dt.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    joblib.dump(dt, 'decision-tree.model')
    print('Model Training Finished. \n \tAccuracy obtained: {}'.format(accuracy))

    return dt



