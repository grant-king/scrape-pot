"""
Daily price data from Diem pot delivery Portland website
Use requests, Beautiful Soup, and Pandas packages to retrieve html data from
https://portland.hellodiem.com/, to locate product information, parse title and
price into lists, remove superfluous pre-sale values, combine into a Pandas
DataFrame, and save to a csv file.

"""

#------------------------------------------------------------------------------
def check_changes(daily_price_df):
    """
    input: dataframe containing daily price data
    output: dictionary of changed products with the most recent change value"""
    changes = {}
    changes_item = []
    changes_value = []
    removed = []

    #check which items have changed price, sold out, or been added
    #using dictionary to avoid duplicates?
    for price in list(daily_price_df.iterrows()):
        for i in range(len(price)):
            #compare each price with its predecessor to determine last change
            if price[1][i] != price[1][i+1]:
                #append the item name and change to 'changes' dictionary
                changes[price[0]] = (price[1][i+1] - price[1][i])
    #
    for item in changes:
        if str(changes[item]) != 'nan':
            changes_item.append(item)
            changes_value.append(changes[item])
        else:
            removed.append(item)

    return [changes_item, changes_value, removed]

def build_df(price_sers):
    today_date = str(dt.date.today())
    combined = pd.concat(price_sers, axis=1)
    #give each column unique name, prices_...
    combined.columns = ['prices_' + str(i) for i in
                        range(1, (len(combined.columns)) + 1)]
    combined.index.name = 'items'
    return combined
#------------------------------------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt

#read filenames
file_list = ['']
filenames_file = open('filenames.txt')
for line in filenames_file:
    file_list.append(line)
filenames_file.close()

"""
file_list = ['prices2018-05-08.csv',
             'prices2018-05-09.csv',
             'prices2018-05-10.csv',
             'prices2018-05-11.csv',
             'prices2018-05-12.csv',
             'prices2018-05-13.csv',
             'prices2018-05-14.csv',
             'prices2018-05-18.csv',
             'prices2018-05-19.csv',
             'prices2018-05-28.csv'
            ]
"""
#read files into dataframes to prepare for combination
pots = [pd.read_csv(file, index_col='item_name') for file in file_list]
pots = [pots[i][['item_price']] for i in range(len(pots))]

#combine into new df
pot_all = build_df(pots)

#print range least to most expensive item and price
print(pot_all.idxmin()[0], ('$' + str(pot_all.loc[pot_all.idxmin()[0]][0])))
print(pot_all.idxmax()[0], ('$' + str(pot_all.loc[pot_all.idxmax()[0]][0])))

items, values, removed = (check_changes(pot_all))

pot_all.boxplot()

plt.show()

changes = pd.DataFrame(values, index=items)
changes.columns = ['net']
print(changes)

#Print list of removed items
for item in removed:
    print(item)

#bool list of all discount ounces
filter_list = pot_all.index.str.contains('DISCOUNT OUNCE', regex=False)

#filter df with list
current_discounts = pot_all[filter_list][pot_all.columns[-1]]

#drop NaNs
current_discounts.dropna()
