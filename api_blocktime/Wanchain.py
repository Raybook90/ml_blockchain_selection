from requests import Request, Session
from general_functions import convert_unix_to_datetime, total_seconds_blocktime_difference


def get_blocktime_wanchain():
    url_info = 'https://wan.tokenview.com/api/coin/latest/wan'

    session = Session()

    blockheight_current = session.get(url_info).json().get('data')
    blockheight_previous = blockheight_current - 1

    url_block_current = 'https://wan.tokenview.com/api/block/wan/%s' % blockheight_current
    url_block_previous = 'https://wan.tokenview.com/api/block/wan/%s' % blockheight_previous

    blocktime_current_unix = session.get(url_block_current).json().get('data')[0].get('time')
    blocktime_previous_unix = session.get(url_block_previous).json().get('data')[0].get('time')

    # Print times of current and previous block to check validity
    # print(convert_unix_to_datetime(blocktime_current_unix))
    # print(convert_unix_to_datetime(blocktime_previous_unix))

    blocktime_difference = convert_unix_to_datetime(blocktime_current_unix - blocktime_previous_unix)

    return total_seconds_blocktime_difference(blocktime_difference)


# print(get_blocktime_wanchain())