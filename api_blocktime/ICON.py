from requests import Request, Session
import json
from datetime import datetime


def get_blocktime_icon():
    url_main_info = 'https://tracker.icon.foundation/v3/main/mainInfo'
    session = Session()

    # get info about current block height
    response_info = session.get(url_main_info)
    main_info_str = json.dumps(response_info.json(), indent=4)

    # Main_info is a string of type JSON formatted data --> deserialize with loads() to convert to dict
    main_info_dict = json.loads(main_info_str)

    blocktime_current = main_info_dict.get('tmainBlock')[0].get('createDate')
    blocktime_previous = main_info_dict.get('tmainBlock')[1].get('createDate')

    fmt = '%Y-%m-%dT%H:%M:%S.%f%z'
    tstamp_current = datetime.strptime(blocktime_current, fmt)
    tstamp_previous = datetime.strptime(blocktime_previous, fmt)
    td = (tstamp_current - tstamp_previous).total_seconds()

    # Print times of current and previous block to check validity
    # print(tstamp_previous)
    # print(tstamp_current)

    return td


# print(get_blocktime_icon())



