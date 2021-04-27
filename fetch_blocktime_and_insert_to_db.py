from db_populate import insertBlocktimeIntoTable
from api.Bitcoin_Ethereum import get_blocktime
from api.Stellar import get_blocktime_stellar
from api.EOS import get_blocktime_eos
from api.Stratis import get_blocktime_stratis
from api.NEO import get_blocktime_neo
from api.Cardano import get_blocktime_cardano
from api.Ripple import get_blocktime_ripple
from api.QTUM import get_blocktime_qtum
from api.ICON import get_blocktime_icon
from api.VeChain import get_blocktime_vechain
from api.Wanchain import get_blocktime_wanchain
import schedule
import time


def insert_rows_every_12mins():
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


# insert_rows_every_12mins()
schedule.every(11).minutes.do(insert_rows_every_12mins)

while True:
    schedule.run_pending()
    time.sleep(1)






