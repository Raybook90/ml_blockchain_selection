import os
from flask import Flask, jsonify, request, render_template
from flask_restful import Api, Resource, reqparse
from model.decisionTree import train_decisiontree
from model.decisionTreeSQLite import train_decision_tree
import joblib
import numpy as np
import sqlite3
import json

app = Flask(__name__)
api = Api(app)

# if not os.path.isfile('decision-tree-without-datasize-feature.model'):
#     train_decisiontree()
#
# model = joblib.load('decision-tree-without-datasize-feature.model')
# label_encoder = joblib.load('label_encoder.joblib')
# dbfile = '../../Desktop/Uzh/Master_Thesis/bcio.db'

if not os.path.isfile('decision-tree-26-02-2021.model'):
    train_decision_tree()

model = joblib.load('decision-tree-26-02-2021.model')
label_encoder = joblib.load('label_encoder.joblib')
dbfile = '../../Desktop/Uzh/Master_Thesis/bcio.db'


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


@app.route('/prediction/', methods=["POST", "GET"])
def prediction():
    return render_template('prediction.html')


@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        dict_type = {'1': 'Public', '0': 'Private'}
        dict_yes_no = {'1': 'Yes', '0': 'No'}
        dict_ordinal = {'1': 'Low', '2': 'Medium', '3': 'High'}

        type = request.form.get('Type')
        smartContract = request.form.get('smartContract')
        turingComplete = request.form.get('turingComplete')
        transactionSpeed = request.form.get('transactionSpeed')
        popularity = request.form.get('popularity')
        minArbitraryData = request.form.get('MinArbitraryData')
        to_predict_list = [int(type), int(smartContract), int(turingComplete), int(transactionSpeed), int(popularity), minArbitraryData]
        selected_blockchain = value_predictor(to_predict_list)
        return render_template("prediction.html", original_input=
        {'Type': dict_type[type],
         'Smart Contracts': dict_yes_no[smartContract],
         'Turing-complete': dict_yes_no[turingComplete],
         'Transaction Speed': dict_ordinal[transactionSpeed],
         'Popularity': dict_ordinal[popularity],
         'Data size': minArbitraryData}, prediction=selected_blockchain)


def value_predictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1,len(to_predict_list))
    prediction_without_label = model.predict(to_predict)
    result_with_label = label_encoder.inverse_transform(prediction_without_label)
    return result_with_label[0]


# Define parser and request args
parser = reqparse.RequestParser()
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


class MakePrediction(Resource):
    @staticmethod
    def post():

        args = parser.parse_args()
        to_predict_list = [args['type'], args['smart_contract'], args['turing_complete'], args['transaction_speed'],
                           args['popularity'], args['data_size']]
        prediction = value_predictor(to_predict_list)
        return jsonify({
            'Prediction': prediction
        })


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
        # return json.dumps([dict(ix) for ix in rows])


# class BlockchainByShortName(Resource):
#     def get(self, shortname):
#         conn = sqlite3.connect(dbfile)
#         cur = conn.cursor()
#


api.add_resource(MakePrediction, '/api/predict')
api.add_resource(Blockchains, '/api/blockchains')


if __name__ == '__main__':
    app.run(debug=True)