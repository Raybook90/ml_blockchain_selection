from api_blocktime.NEO import convert_unix_to_datetime, total_seconds_blocktime_difference
from requests import Request, Session


def get_blocktime_stratis():
    # URLs for get requests
    url_blockcount = 'https://chainz.cryptoid.info/strax/api.dws?q=getblockcount'
    url_blocktime = 'https://chainz.cryptoid.info/strax/api.dws?q=getblocktime'

    session = Session()

    # get info about current block count
    response_blockcount = session.get(url_blockcount)

    current_blockheight = response_blockcount.text
    previous_blockheight = int(current_blockheight) - 1
    # print(current_blockheight)

    parameter = {
        'height': current_blockheight
    }

    response_blocktime_current = session.get(url_blocktime, params=parameter)
    response_blocktime_previous = session.get(url_blocktime, params={'height': previous_blockheight})

    current_blocktime_unixtime = int(response_blocktime_current.text)
    previous_blocktime_unixtime = int(response_blocktime_previous.text)

    #Print times of current and previous block to check validity
    current_blocktime = convert_unix_to_datetime(current_blocktime_unixtime)
    previous_blocktime = convert_unix_to_datetime(previous_blocktime_unixtime)
    # print(current_blocktime)
    # print(previous_blocktime)

    # get difference of blocktime current and previous UNIX
    blocktime_difference_UNIX = current_blocktime_unixtime - previous_blocktime_unixtime

    # Convert UNIX time to datetime
    blocktime_difference = convert_unix_to_datetime(blocktime_difference_UNIX)

    return total_seconds_blocktime_difference(blocktime_difference)
