from api_blocktime.NEO import convert_unix_to_datetime, total_seconds_blocktime_difference
from requests import Session
from datetime import datetime


def get_blocktime_qtum():
    url_info = 'https://qtum.info/api/info/'

    session = Session()
    # get info about current block
    response = session.get(url_info)
    info = response.json()

    # current block height
    current_blockheight = info.get('height')
    # print(current_blockheight)

    url_block_current = 'https://qtum.info/api/block/%s' % current_blockheight
    url_block_previous = 'https://qtum.info/api/block/%s' % (current_blockheight - 1)

    block_data_current = session.get(url_block_current).json()
    block_data_previous = session.get(url_block_previous).json()

    blocktime_current_unix = block_data_current.get('timestamp')
    blocktime_previous_unix = block_data_previous.get('timestamp')

    # get difference of blocktime current and previous UNIX
    blocktime_difference_unix = blocktime_current_unix - blocktime_previous_unix

    # Convert UNIX time to datetime
    blocktime_difference = convert_unix_to_datetime(blocktime_difference_unix)

    return total_seconds_blocktime_difference(blocktime_difference)
