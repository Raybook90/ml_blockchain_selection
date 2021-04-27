from requests import Request, Session
from datetime import datetime


def get_blocktime_eos ():
    url_info = 'https://bp.cryptolions.io/v1/chain/get_info'
    url_block = 'https://bp.cryptolions.io/v1/chain/get_block'
    session = Session()

    # get info about current block
    response_info = session.get(url_info)

    # Extract data in json format
    info = response_info.json()

    # Use current block num from info to get block information (timestamp)
    parameter_header_block = {"block_num_or_id": info["head_block_num"]}
    # print(parameter_header_block)
    # Get head block info
    response_block_head = session.get(url_block, json= parameter_header_block)

    # Extract data in json format
    head = response_block_head.json()

    # Increment block num by 1 in order to compare timestamps from two consecutive blocks
    parameter_previous_block = parameter_header_block.copy()
    parameter_previous_block["block_num_or_id"] -= 1

    # Get previous block info
    response_previous_block = session.get(url_block, json= parameter_previous_block)

    # Extract data in json format
    previous = response_previous_block.json()

    fmt = '%Y-%m-%dT%H:%M:%S.%f'

    tstamp_head = datetime.strptime(head['timestamp'], fmt)
    tstamp_previous = datetime.strptime(previous['timestamp'], fmt)
    td = (tstamp_head - tstamp_previous).total_seconds()

    return td



