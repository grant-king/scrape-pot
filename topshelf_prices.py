def strip_product(header_list):
    """input a list of tag-type values and return list of strings with surrounding html characters removed"""

    string_list = ['' for item in range(len(header_list))]
    for item in range(len(header_list)):
        string_list[item] = str(header_list[item])[53:-14]
    return string_list

def strip_price(header_list):
    """input a list of tag-type values and return list of strings with surrounding html characters removed"""
    import re
    match_obs = []
    regex = '\$(((\d+).\d+)|(\d+))'

    string_list = []#['' for item in range(len(header_list))]

    for item in range(len(header_list)):
        match_obs.append(re.search(regex, str(header_list[item])))

    for i in range(len(match_obs)):
        #print(match_obs[i])
        string_list.append(match_obs[i].group(1))
    #print(string_list)
    return string_list

def get_heading_list(url):
    # Packages the request, send the request and catch the response: r
    r = requests.get(url)
    html_text = r.text

    #set soup list equal to html text from page
    soup = BeautifulSoup(html_text, 'html.parser')

    headings = [[], []]
    #get list of product title headings on page
    headings[0] = soup.find_all('div', class_='flex list-item-title')

    #create navigable match object for all prices, but will just need one per product
    match_obs = soup.find_all('div', class_='layout hidden-sm-and-down row')

    #append appropriate header to list
    for i in range(len(match_obs)):
        #price per quarter oz, no tax
        headings[1].append(match_obs[i].contents[4].div)
    return headings

def save_csv(pot_df):
    #import datetime, needed to get current date
    import datetime as dt
    #set today_date, formatted as YYYY-MM-DD
    today_date = str(dt.date.today())
    #print(today_date)
    #write to csv and set index to position rather than name, use
    pot_df.to_csv(('topshelf_'+ today_date +'.csv'), encoding='utf8',
    header=['item_name', 'item_price'], index_label='relative_position')

def call_warning():
    """called when save has failed"""
    from tkinter import messagebox
    messagebox.showerror("Error", "Lists not equal length; save failed")

from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://www.topshelfbudz.com/flower/'
#lists to hold lists of headers, one for each page
all_products = []
all_prices = []

#iterate over each list of headers for a page, set each index of headers is a list
headers = get_heading_list(url)

#strip html tag data from header lists
all_products.append(strip_product(headers[0]))
all_prices.append(strip_price(headers[1]))

#convert lists to series
product_ser = pd.Series(all_products[0])
price_ser = pd.Series(all_prices[0])
together = pd.DataFrame([product_ser, price_ser]).T
print(together)
#validate data congruency before saving to csv
if len(all_products) == len(all_prices):
    save_csv(together)
else:
    call_warning()
