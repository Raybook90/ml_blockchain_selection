from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import RandomOverSampler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import joblib
import pandas as pd
import sqlite3


def train_models():
    con = sqlite3.connect('../bcio.db')
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

    # Oversample minority classes with RandomOverSampler
    ros = RandomOverSampler(random_state=777)
    X_ROS, y_ROS = ros.fit_resample(X,y)

    # Instantiate LabelEncoder and transform target values
    le = LabelEncoder()
    y_ROS = le.fit_transform(y_ROS)

    # Serialize LabelEncoder with joblib
    joblib.dump(le, 'label_encoder.joblib')

    # Train Decision Tree
    dt = DecisionTreeClassifier().fit(X_ROS, y_ROS)

    # Serialize decision tree model
    joblib.dump(dt, 'decision-tree.model')

    # Train Random Forest
    rf = RandomForestClassifier(n_estimators=20).fit(X_ROS, y_ROS)
    joblib.dump(rf, 'random-forest.model')

    # Train Naive Bayes
    nb_clf = MultinomialNB().fit(X_ROS, y_ROS)
    joblib.dump(nb_clf, 'naive-bayes.model')

    # Train Support Vector Machine
    svm_clf = SVC(kernel='linear', C=1).fit(X_ROS, y_ROS)
    joblib.dump(svm_clf, 'svm.model')

    return

