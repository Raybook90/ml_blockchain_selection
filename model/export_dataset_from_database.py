import pandas as pd
import sqlite3

con = sqlite3.connect('bcio.db')

query = """
    SELECT name as blockchain, type, smart_contract, turing_complete, platform_transaction_speed, popularity, MinArbitraryData
            FROM blockchains_for_dataset
            NATURAL JOIN attributes_for_dataset
"""

data = pd.read_sql_query(query, con)
data.to_csv('dataset.csv', index=False)
