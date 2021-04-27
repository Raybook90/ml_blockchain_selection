from requests import Session
from datetime import datetime


def convert_unix_to_datetime(time):
    return datetime.utcfromtimestamp(time).strftime('%H:%M:%S')


def total_seconds_blocktime_difference(time):
    a = time.split(':')
    return int(a[0])*3600 + int(a[1]) * 60 + int(a[2])


def get_blocktime_neo():

    url_blockheight = 'https://api.neoscan.io/api/main_net/v1/get_height'
    session = Session()
    # get info about current block height
    current_blockheight = session.get(url_blockheight).json().get('height')
    # print(current_blockheight)

    # get block time for current blockheight and previous blockheight
    url_block_current = 'https://api.neoscan.io/api/main_net/v1/get_block/%s' % current_blockheight
    url_block_previous = 'https://api.neoscan.io/api/main_net/v1/get_block/%s' % (current_blockheight -1)

    blocktime_current_unix = session.get(url_block_current).json().get('time')
    blocktime_previous_unix = session.get(url_block_previous).json().get('time')

    # get difference of blocktime current and previous UNIX
    blocktime_difference_unix = blocktime_current_unix - blocktime_previous_unix

    # Convert UNIX time to datetime
    blocktime_difference = convert_unix_to_datetime(blocktime_difference_unix)

    return total_seconds_blocktime_difference(blocktime_difference)
