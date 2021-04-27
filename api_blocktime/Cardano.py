from api_blocktime.NEO import total_seconds_blocktime_difference
from requests import Request, Session
from datetime import datetime


def get_blocktime_cardano():
    url_stats = 'https://api.blockchair.com/cardano/stats'
    session = Session()
    # get info about current block count
    response_stats = session.get(url_stats)
    stats = response_stats.json()
    current_blockheight = stats.get('data').get('best_block_height')

    url_block_current = 'https://api.blockchair.com/cardano/raw/block/%s' % current_blockheight
    url_block_previous = 'https://api.blockchair.com/cardano/raw/block/%s' % (current_blockheight - 1)

    response_current_block = session.get(url_block_current)
    block_data_current = response_current_block.json()
    response_previous_block = session.get(url_block_previous)
    block_data_previous = response_previous_block.json()

    blocktime_UNIX_current = block_data_current.get('data').get(str(current_blockheight)).get('block').get('cbsEntry').get('cbeTimeIssued')
    blocktime_UNIX_previous = block_data_previous.get('data').get(str(current_blockheight-1)).get('block').get('cbsEntry').get('cbeTimeIssued')

    # get difference of blocktime current and previous UNIX
    blocktime_difference_UNIX = blocktime_UNIX_current - blocktime_UNIX_previous

    # Convert UNIX time to datetime
    blocktime_difference = datetime.utcfromtimestamp(blocktime_difference_UNIX).strftime('%H:%M:%S')

    return total_seconds_blocktime_difference(blocktime_difference)

