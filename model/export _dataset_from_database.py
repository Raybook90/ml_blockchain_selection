import pandas as pd
import sqlite3

con = sqlite3.connect('../../../Desktop/Uzh/Master_Thesis/bcio.db')

# query = """
# SELECT * from dataset;
# """

query = """
    SELECT name as blockchain, type, smart_contract, turing_complete, platform_transaction_speed, popularity, MinArbitraryData
            FROM blockchains_for_dataset
            NATURAL JOIN attributes_for_dataset
"""

data = pd.read_sql_query(query, con)

# data = data.drop('blocktime', axis='columns')

data.to_csv('dataset24feb2021.csv', index=False)