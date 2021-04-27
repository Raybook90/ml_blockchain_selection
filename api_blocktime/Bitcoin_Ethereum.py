import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import sqlite3
                              

#print(crypto_stats)
# blocktime = page_soup.findAll("tr", {"id":"t_time"})
#
# print(blocktime)


def get_blocktime(blockchain):
    url = 'https://bitinfocharts.com/'

    # Make a GET request to fetch the raw HTML content
    html_content = requests.get(url).text

    # Parse HTML code for the entire site
    soup = BeautifulSoup(html_content, 'lxml')
    # print the parsed data of html
    # print(soup.prettify())

    # On site there is 1 table with class "table body"
    crypto_stats = soup.find_all("tr")

    # Head values (Column names) are the first items of the body list
    head = crypto_stats[0]  # 0th item is the header row
    body_rows = crypto_stats[1:]  # All other items becomes the rest of the rows

    # Lets now iterate through the head HTML code and make list of clean headings
    headings = []
    for item in head.find_all("td"):  # loop through all td elements in head
        # convert the td elements to text and strip "\n"
        item = (item.text).rstrip("\n")
        item = item.strip()
        # append the clean column name to headings
        headings.append(item)

    headings[0] = 'Attributes'

    # loop through the rest of the rows

    all_rows = []  # will be a list for list for all rows
    for row_num in range(len(body_rows)):  # A row at a time
        row = []  # this will add entries for one row
        for row_item in body_rows[row_num].find_all("td"):  # loop through all row entries
            # row_item.text removes the tags from the entries
            # the reges is to remove \xa0 and \n and comma from row_item.text
            # xa0 encodes the flag, \n is the newline and comma separates thousands in numbers
            aa = re.sub("(\xa0) | (\n) |,", "", row_item.text)
            # append aa to row - note one row entry is being appended
            row.append(aa)
        # append one row to all_rows
        all_rows.append(row)

    # Use data on all_rows and headings to make a table
    # all_rows becomes our data and headings the column names
    df = pd.DataFrame(data=all_rows, columns=headings)

    df = df.drop(['Litecoin(Explorer, top100)', 'Bitcoin Cash(Explorer, top100)', 'Bitcoin SV(Explorer, top100)',
                  'Monero', 'Dash(Explorer, top100)', 'Zcash', 'Ethereum Classic', 'Dogecoin(Explorer, top100)',
                  'Bitcoin Gold(Explorer, top100)', 'Reddcoin(Explorer, top100)', 'Vertcoin(Explorer, top100)',
                  'Namecoin(Explorer, top100)', 'Blackcoin(Explorer, top100)', 'Feathercoin(Explorer, top100)',
                  'Novacoin(Explorer, top100)'], 1)

    pd.set_option("display.max_rows", None, "display.max_columns", None)
    df.rename(columns={'Bitcoin(Explorer, top100)': 'Bitcoin'}, inplace=True)

    df_blocktime = df[df['Attributes'] == 'Block Time']
    blocktime_target = df_blocktime.iloc[0][blockchain]
    if len(blocktime_target.split()) == 2:
        m_s = blocktime_target.split()
        minutes = float(m_s[0][:-1])
        seconds = float(m_s[1][:-1])
        total_seconds = minutes * 60 + seconds
    else:
        total_seconds = float(blocktime_target[:-1])
    return total_seconds


# print(get_blocktime('Ethereum'))


# def get_tps(blockchain):
#     df_tps = df[df['Attributes'] == 'Transactions avg. per hour']
#     tps_target = df_tps.iloc[0][blockchain]
#     return float(tps_target)/3600




