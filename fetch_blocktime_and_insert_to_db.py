from api_blocktime.Bitcoin_Ethereum import get_blocktime
from api_blocktime.Stellar import get_blocktime_stellar
from api_blocktime.EOS import get_blocktime_eos
from api_blocktime.Stratis import get_blocktime_stratis
from api_blocktime.NEO import get_blocktime_neo
from api_blocktime.Cardano import get_blocktime_cardano
from api_blocktime.Ripple import get_blocktime_ripple
from api_blocktime.QTUM import get_blocktime_qtum
from api_blocktime.ICON import get_blocktime_icon
from api_blocktime.VeChain import get_blocktime_vechain
from api_blocktime.Wanchain import get_blocktime_wanchain
import schedule
import time
import sqlite3


def insertBlocktimeIntoTable(name, time):
    try:
        sqliteConnection = sqlite3.connect('bcio.db')
        cursor = sqliteConnection.cursor()
        # print("Successfully connected to database")

        sqlite_insert_query = '''INSERT INTO blocktime(blockchain, blocktime)
        VALUES(?,?)'''

        data = (name, time)
        cursor.execute(sqlite_insert_query, data)
        sqliteConnection.commit()
        # print("Record inserted successfully into attributes_for_dataset table")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data ino sqlite table", error)
    finally:
        if(sqliteConnection):
            sqliteConnection.close()
            # print("The SQLite connection is closed")


def insert_rows():
    insertBlocktimeIntoTable('Bitcoin', get_blocktime('Bitcoin'))
    insertBlocktimeIntoTable('Ethereum', get_blocktime('Ethereum'))
    insertBlocktimeIntoTable('Stellar', get_blocktime_stellar())
    insertBlocktimeIntoTable('EOS', get_blocktime_eos())
    insertBlocktimeIntoTable('NEO', get_blocktime_neo())
    insertBlocktimeIntoTable('Cardano', get_blocktime_cardano())
    insertBlocktimeIntoTable('Ripple', get_blocktime_ripple())
    insertBlocktimeIntoTable('QTUM', get_blocktime_qtum())
    insertBlocktimeIntoTable('ICON', get_blocktime_icon())
    insertBlocktimeIntoTable('VeChain', get_blocktime_vechain())
    # insertBlocktimeIntoTable('Wanchain', get_blocktime_wanchain())
    print('Rows have successfully been added to the dataset')


insert_rows()
# insert rows every 11 minutes
schedule.every(11).minutes.do(insert_rows)

while True:
    schedule.run_pending()
    time.sleep(1)






