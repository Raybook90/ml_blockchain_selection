from general_functions import *
from requests import Session


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

    # Print times of current and previous block to check validity
    # print(convert_unix_to_datetime(blocktime_current_unix))
    # print(convert_unix_to_datetime(blocktime_previous_unix))

    # get difference of blocktime current and previous UNIX
    blocktime_difference_unix = blocktime_current_unix - blocktime_previous_unix

    # Convert UNIX time to datetime
    blocktime_difference = convert_unix_to_datetime(blocktime_difference_unix)

    return total_seconds_blocktime_difference(blocktime_difference)

# print(get_blocktime_neo())