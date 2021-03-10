from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import joblib
import pandas as pd
import sqlite3


def train_decision_tree():
    con = sqlite3.connect('../../Desktop/Uzh/Master_Thesis/bcio.db')
    query = "SELECT name as blockchain, type, smart_contract, turing_complete, platform_transaction_speed, popularity, " \
            "MinArbitraryData FROM blockchains_for_dataset NATURAL JOIN attributes_for_dataset"
    raw_data = pd.read_sql_query(query, con)
    con.close()

    # Compare one BC with all others, and if other BC has higher MinArbitraryData value, copy and add row to list with
    # the lower MinArbitraryData value
    new_rows = []
    for index, row in raw_data.iterrows():
        for ind, r in raw_data.iterrows():
            if row.MinArbitraryData <= r.MinArbitraryData and row.blockchain != r.blockchain:
                newrow = raw_data.loc[ind].copy()
                newrow.MinArbitraryData = row.MinArbitraryData
                new_rows.append(newrow.values)

    new_rows_df = pd.DataFrame(new_rows, columns=raw_data.columns)

    # Concatenate the two dataframes
    df = pd.concat([raw_data, new_rows_df])

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

    # Serialize LabelEncoder with pickle
    #pickle.dump(le, open('label_encoder.obj', 'wb'))

    # Serialize LabelEncoder with joblib
    joblib.dump(le, 'label_encoder.joblib')

    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # Train decision tree
    dt = DecisionTreeClassifier().fit(X, y)
    # predictions = dt.predict(X_test)
    # accuracy = accuracy_score(y_test, predictions)
    # print('Model Training Finished. \n \tAccuracy obtained: {}'.format(accuracy))

    # Serialize decision tree model
    joblib.dump(dt, 'decision-tree-26-02-2021.model')

    #  Train naive bayes classifier
    nb_clf = MultinomialNB().fit(X,y)
    joblib.dump(nb_clf, 'naive-bayes.model')

    return dt

