#------------------------------------------------------------------------------
#Functions
#------------------------------------------------------------------------------
def get_heading_list(url, page):
    """Get all headings matching a particular pattern from the indicated page
    and url. Paramaters allow for calling different subdomains of the same
    site, provided they have identical styles"""
    # Packages the request, send the request and catch the response: r
    r = requests.get(url+'page/'+str(page)+'/')
    html_text = r.text

    #set soup list equal to html text from page
    soup = BeautifulSoup(html_text, 'html.parser')

    headings = [[], []]
    #get list of product title headings on page
    headings[0] = soup.find_all('h2', class_='woocommerce-loop-product__title')

    #get list of product price headings on page
    headings[1] = soup.find_all('span',
        class_='woocommerce-Price-amount amount')
    pop_presale_price(headings[1])
    return headings

def pop_presale_price(price_headings):
    """helper function to remove extra pre-sale prices from final list. Input
    list of headers, get back list of headers less those that had a particular
    tag"""
    for item in price_headings:
        if item.parent.name == 'del':
            price_headings.pop(price_headings.index(item))

def strip_product(header_list):
    """input a list of tag-type values and return list of strings with
    surrounding html characters removed"""
    string_list = ['' for item in range(len(header_list))]
    for item in range(len(header_list)):
        string_list[item] = str(header_list[item])[44:-5]
    return string_list

def strip_price(header_list):
    """input a list of tag-type values and return list of strings with
    surrounding html characters removed"""
    string_list = ['' for item in range(len(header_list))]
    for item in range(len(header_list)):
        string_list[item] = str(header_list[item])[101:-7]
    return string_list

def build_df(price_sers):
    today_date = str(dt.date.today())
    combined = pd.concat(price_sers, axis=1)
    #give each column unique name, prices_...
    combined.columns = ['prices_' + str(i) for i in
                        range(1, (len(combined.columns)) + 1)]
    combined.index.name = 'items'
    return combined

#------------------------------------------------------------------------------
#Imports
#------------------------------------------------------------------------------
from bs4 import BeautifulSoup
import requests
import pandas as pd

#------------------------------------------------------------------------------
#Main
#------------------------------------------------------------------------------
max_page = 8
url = 'https://portland.hellodiem.com/'
url_2 = 'https://salem.hellodiem.com/'

#create a list to hold lists of headers, one for each page
h_product = ['' for strng in range(max_page)]
h_price = ['' for strng in range(max_page)]

#iterate over each list of headers for a page, set each index of headers equal
#to list
for page in range(0, max_page):
    headers = get_heading_list(url, page+1)
    h_product[page] = headers[0]
    h_price[page] = headers[1]

combined_products = []
combined_prices = []

for sublist in range(max_page):
    combined_products.append(strip_product(h_product[sublist]))

for sublist in range(max_page):
    combined_prices.append(strip_price(h_price[sublist]))

#create a list of all prices
all_prices = []
for by_page in combined_prices:
    for li in by_page:
        #print(li, '\n')
        all_prices.append(float(li))

#create a list of all products
all_products = []
for by_page in combined_products:
    for li in by_page:
        #print(li, '\n')
        all_products.append(li)


product_ser = pd.Series(all_products)
price_ser = pd.Series(all_prices)

pot = pd.DataFrame([product_ser, price_ser]).T

#import datetime, needed to get current date
import datetime as dt
#set today_date, formatted as YYYY-MM-DD
today_date = str(dt.date.today())
#print(today_date)

#write to csv and set index to position rather than name, use
pot.to_csv(('prices'+ today_date +'.csv'), encoding='utf8',
           header=['item_name', 'item_price'], index_label='relative_position')

#pot.to_csv(('prices_salem'+ today_date +'.csv'), encoding='utf8',
#           header=['item_name', 'item_price'], index_label='relative_position')

#------------------------------------------------------------------------------
