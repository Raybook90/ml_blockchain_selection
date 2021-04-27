from requests import Request, Session
from general_functions import convert_unix_to_datetime, total_seconds_blocktime_difference

def get_blocktime_vechain():

    url_main_info = 'https://explore.vechain.org/api/blocks/best'

    session = Session()

    # get info about current block height
    response_info = session.get(url_main_info).json()
    blockheight_current = response_info.get('block').get('number')
    blockheight_previous = blockheight_current - 1

    url_previous_block = 'https://explore.vechain.org/api/blocks/%s' % blockheight_previous

    blocktime_previous_unix = session.get(url_previous_block).json().get('block').get('timestamp')
    blocktime_current_unix = response_info.get('block').get('timestamp')

    # Print times of current and previous block to check validity
    # print(convert_unix_to_datetime(blocktime_current_unix))
    # print(convert_unix_to_datetime(blocktime_previous_unix))

    blocktime_difference_UNIX = blocktime_current_unix - blocktime_previous_unix

    # Convert UNIX time to datetime
    blocktime_difference = convert_unix_to_datetime(blocktime_difference_UNIX)

    return total_seconds_blocktime_difference(blocktime_difference)


# print(get_blocktime_vechain())