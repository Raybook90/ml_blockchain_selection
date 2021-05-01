# import required libraries
import os
from flask import Flask, jsonify, request, render_template
from flask_restful import Api, Resource, reqparse
from model.trainModelsFromSQLite import train_models
import joblib
import numpy as np
import sqlite3
import json

# Instantiate Flask server and initialize Api object
app = Flask(__name__)
api = Api(app)

# Check if models are already trained; if not --> train models
if not os.path.isfile('decision-tree.model'):
    train_models()

# Use joblib to load the trained models
# Decision tree
dt_model = joblib.load('decision-tree.model')
# Random Forest
rf_model = joblib.load('random-forest.model')
# Support Vector Machine
svm_model = joblib.load('svm.model')
# Naive Bayes
nb_model = joblib.load('naive-bayes.model')

# Load label encoder to reconvert numeric labels back into the respective category (BC name)
label_encoder = joblib.load('label_encoder.joblib')
dbfile = 'bcio.db'


# This route will display the website homepage where the available BCs and their properties are displayed
# (function serves up the available_blockchains.html)
@app.route("/")
def home():
    block_data = query_available_blockchains()
    return render_template("available_blockchains.html", block_data=block_data)


def query_available_blockchains():
    conn = sqlite3.connect(dbfile)
    cur = conn.cursor()
    cur.execute("""
    SELECT name, type, blocktime, tps, smart_contract, turing_complete, platform_transaction_speed, popularity, MinArbitraryData 
            FROM blockchains_for_dataset
            NATURAL JOIN attributes_for_dataset
    """)
    data = cur.fetchall()
    return data


# Route for collection of input variables for model prediction (from webpage)
@app.route('/prediction/', methods=["POST", "GET"])
def prediction():
    return render_template('prediction.html')


# Route that receives POST request from Webpage, with the user input, it extracts the input and use the blockchain_predictor
# to get a result and finally render prediction.html with the results in place
@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        dict_type = {'1': 'Public', '0': 'Private'}
        dict_yes_no = {'1': 'Yes', '0': 'No'}
        dict_ordinal = {'1': 'Low', '2': 'Medium', '3': 'High'}
        dict_model = {'decision_tree': 'Decision Tree', 'random_forest': 'Random Forest', 'naive_bayes': 'Naive Bayes',
                      'support_vector_machine': 'Support Vector Machine'}

        model = request.form.get('model')
        type = request.form.get('Type')
        smartContract = request.form.get('smartContract')
        turingComplete = request.form.get('turingComplete')
        transactionSpeed = request.form.get('transactionSpeed')
        popularity = request.form.get('popularity')
        minArbitraryData = request.form.get('MinArbitraryData')
        to_predict_list = [model, int(type), int(smartContract), int(turingComplete), int(transactionSpeed), int(popularity), minArbitraryData]
        selected_blockchain = blockchain_predictor(to_predict_list)
        return render_template("prediction.html", original_input=
        {'Model': dict_model[model],
         'Type': dict_type[type],
         'Smart Contracts': dict_yes_no[smartContract],
         'Turing-complete': dict_yes_no[turingComplete],
         'Transaction Speed': dict_ordinal[transactionSpeed],
         'Popularity': dict_ordinal[popularity],
         'Data size': minArbitraryData}, prediction=selected_blockchain)


# Prediction function takes list with input variables and converts it into numpy array to be fit into the model.
# Depending on the model that was selected, the respective model is used for prediction. Finally, the loaded
# label encoder is used to reconvert the output value from numeric back into the respective category (BC name).
def blockchain_predictor(to_predict_list):
    # Convert input to array
    features = [np.array(to_predict_list[1:])]
    chosen_model = to_predict_list[0]
    if chosen_model == 'decision_tree':
        prediction = dt_model.predict(features)
    elif chosen_model == 'random_forest':
        prediction = rf_model.predict(features)
    elif chosen_model == 'support_vector_machine':
        prediction = svm_model.predict(features)
    else:
        prediction = nb_model.predict(features)
    # Inverse transform to get the original dependent value
    prediction_decoded = label_encoder.inverse_transform(prediction)
    return prediction_decoded[0]


# Route handler for prediction endpoint via PleBeuS
class MakePrediction(Resource):
    @staticmethod
    def post():
        # Define parser and request args
        parser = reqparse.RequestParser()
        parser.add_argument("model", type=str, help="Please choose which ML algorithm to use", required=True,
                            location='json')
        parser.add_argument("type", type=int, help="Preferred Type of BC is required", required=True,
                            location='json')
        parser.add_argument("smart_contract", type=int, help="Smart Contract Supportability is required",
                            required=True, location='json')
        parser.add_argument("turing_complete", type=int, help="Turing Completeness is required", required=True,
                            location='json')
        parser.add_argument("transaction_speed", type=int, help="Transaction Speed is required", required=True,
                            location='json')
        parser.add_argument("popularity", type=int, help="Popularity is required", required=True,
                            location='json')
        parser.add_argument("data_size", type=int, help="Please specify minimum amount of data (bytes) that "
                                                        "should be supported", required=True, location='json')
        args = parser.parse_args()
        # Convert input to list
        to_predict_list = [args['model'], args['type'], args['smart_contract'], args['turing_complete'], args['transaction_speed'],
                           args['popularity'], args['data_size']]
        # Send input variables to blockchain_predictor method, where the loaded model is applied and the prediction is made
        prediction = blockchain_predictor(to_predict_list)
        blockchain_shortname = {
            'Bitcoin': 'BTC',
            'Ethereum': 'ETH',
            'Stellar': 'XLM',
            'EOS': 'EOS',
            'IOTA': 'MIOTA',
            'Hyperledger': 'HYP',
            'Multichain': 'MLC',
            'R3 Corda': 'COR',
            'Stratis': 'STRAX',
            'Neo': 'NEO',
            'Cardano': 'ADA',
            'Ripple': 'XRP',
            'QTUM': 'QTUM',
            'ICON': 'ICX',
            'VeChain': 'VET',
            'Wanchain': 'WAN'
        }
        return jsonify({
            'name': blockchain_shortname[prediction]
        })


# Route handler to get all available BCs and their properties
class Blockchains(Resource):
    @staticmethod
    def get():
        conn = sqlite3.connect(dbfile)
        cur = conn.cursor()
        cur.execute("""
            SELECT name, type, blocktime, tps, smart_contract, turing_complete, platform_transaction_speed, popularity, 
            MinArbitraryData as data_size
            FROM blockchains_for_dataset
            NATURAL JOIN attributes_for_dataset
        """)

        row_headers = [x[0] for x in cur.description] #extract row headers
        rv = cur.fetchall()
        conn.commit()
        conn.close()
        json_data=[]
        for row in rv:
            json_data.append(dict(zip(row_headers,row)))
        return jsonify(json_data)


# Add API endpoints
api.add_resource(MakePrediction, '/api/predict')
api.add_resource(Blockchains, '/api/blockchains')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')