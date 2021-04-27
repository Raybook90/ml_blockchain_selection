from requests import Request, Session
from datetime import datetime


def get_blocktime_stellar():
    url_stats = 'https://api.blockchair.com/stellar/stats'
    session = Session()
    # get info about current block count
    response_stats = session.get(url_stats)
    stats = response_stats.json()
    current_blockheight = stats.get('data').get('best_ledger_height')

    url_block_current = 'https://api.blockchair.com/stellar/raw/ledger/%s' % current_blockheight
    url_block_previous = 'https://api.blockchair.com/stellar/raw/ledger/%s' % (current_blockheight - 1)

    response_current_block = session.get(url_block_current)
    block_data_current = response_current_block.json()
    response_previous_block = session.get(url_block_previous)
    block_data_previous = response_previous_block.json()

    blocktime_current = block_data_current.get('data').get(str(current_blockheight)).get('ledger').get('closed_at')
    blocktime_previous = block_data_previous.get('data').get(str(current_blockheight-1)).get('ledger').get('closed_at')

    fmt = '%Y-%m-%dT%H:%M:%SZ'
    tstamp_current = datetime.strptime(blocktime_current, fmt)
    tstamp_previous = datetime.strptime(blocktime_previous, fmt)
    td = (tstamp_current - tstamp_previous).total_seconds()

    return td


