from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

def scrape(imo_numbers):
    # set user-agent to access webpage
    header = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"}
    # classes to find
    to_find = ["v4 is-hidden-mobile", "v6 is-hidden-mobile"]
    # create dataframe to store scraped data
    scraped = pd.DataFrame( columns=['imo', 'length'])

    for imo_number in imo_numbers:
        # while loop with try and except to avoid connection errors
        while True:
            try:
                # set url and get html code
                url = 'https://www.vesselfinder.com/vessels?name=' + str(imo_number)
                html = requests.get(url, headers=header)
                soup = BeautifulSoup(html.text, 'lxml')
                # scrape and save data we are looking for (if exists)
                if soup.find('td', class_ = to_find[0]) is not None:
                    length_and_width = soup.find('td', class_ = to_find[1]).text
                    length = length_and_width.split(' ')[0]
                    if length.isnumeric()==False:
                        length = np.nan
                    scraped = scraped.append([{'imo': imo_number, 'length': length}])
                    break
                # set all data to np.nan (if not exist)
                else:
                    length = np.nan
                    imo_number = np.nan
                    break
            except:
                None

    # save scraped data to csv file
    scraped.to_csv('data\scraped_length.csv', sep=',', index=False)