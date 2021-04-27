from general_functions import *
from requests import Request, Session
from datetime import datetime

def get_blocktime_ripple():
    url_stats = 'https://api.blockchair.com/ripple/stats'
    session = Session()
    # get info about current block count
    response_stats = session.get(url_stats)
    stats = response_stats.json()
    current_blockheight = stats.get('data').get('best_ledger_height')

    url_block_current = 'https://api.blockchair.com/ripple/raw/ledger/%s' % current_blockheight
    url_block_previous = 'https://api.blockchair.com/ripple/raw/ledger/%s' % (current_blockheight - 1)

    response_current_block = session.get(url_block_current)
    block_data_current = response_current_block.json()
    response_previous_block = session.get(url_block_previous)
    block_data_previous = response_previous_block.json()

    blocktime_current_unix = block_data_current.get('data').get(str(current_blockheight)).get('ledger').get('close_time')
    blocktime_previous_unix = block_data_previous.get('data').get(str(current_blockheight-1)).get('ledger').get('close_time')

    # Print times of current and previous block to check validity
    # print(convert_unix_to_datetime(blocktime_current_unix))
    # print(convert_unix_to_datetime(blocktime_previous_unix))

    # get difference of blocktime current and previous UNIX
    blocktime_difference_unix = blocktime_current_unix - blocktime_previous_unix

    # Convert UNIX time to datetime
    blocktime_difference = convert_unix_to_datetime(blocktime_difference_unix)

    return total_seconds_blocktime_difference(blocktime_difference)


# print(get_blocktime_ripple())
