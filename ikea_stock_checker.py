import requests as req
from bs4 import BeautifulSoup as BS
import sys
import os
import time
from pprint import pprint

def execution_help():
    print("Arguments: <required 8-digit product code> <optional 3-digit store code(s)> ...")
    print("No store code argument(s) will return product availability results for all US stores.")
    print("Only 1 product may be requested at once.")
    exit()

def check_valid_args_syntax(product_code, store_id_list):
    if len(product_code) != 8:
        execution_help()
    for id in store_id_list:
        if len(id) != 3:
            execution_help()

def get_store_stock(soup, store_id_list):
    stores = []

    for store_tag in soup.find_all('localstore'):
        store = {}

        store['_store_id'] = int(store_tag.attrs['bucode'])
        store['available_stock'] = int(store_tag.find('availablestock').contents[0])
        store['in_stock_probability'] = store_tag.find('instockprobabilitycode').contents[0]

        restock_date = store_tag.find('restockdate')
        if restock_date is not None:
            store['restock_date'] = restock_date.contents[0]
        else:
            store['restock_date'] = None

        i = 1
        for fc in store_tag.find('forecasts').contents:
            four_forecasts = {}
            date = fc.find('validdate').contents[0]
            stock = fc.find('availablestock').contents[0]
            four_forecasts['forecast_date'] = date
            four_forecasts['forecast_stock'] = int(stock)
            key = ['forecast', str(i)]
            key_name = '_'.join(key)
            store[key_name] = four_forecasts        # problem line
            i = i + 1

        stores.append(store)

    return stores

def main():
    BASE_URL = "https://www.ikea.com/us/en/iows/catalog/availability/"

    product_code = sys.argv[1]
    store_id_list = sys.argv[2:]

    check_valid_args_syntax(product_code, store_id_list)

    r = req.get(BASE_URL + product_code)
    soup = BS(r.text, 'lxml')

    dir_path = os.path.dirname(os.path.realpath(__file__))
    last_modified_time = os.path.getmtime(dir_path + '/stores.txt')
    current_time = time.time()

    stores = get_store_stock(soup, store_id_list)
    r.close()

    if (current_time - last_modified_time) > 60: #21600
        try:
            f = open("stores.txt", "w")
        except FileNotFoundError: 
            f = open("stores.txt", "x")
        f.write(str(stores))
        f.close()

    store_not_exist = []
    for store_id in store_id_list:
        try:
            pprint(next(item for item in stores if item['_store_id'] == int(store_id)))
            print()
        except StopIteration:
            store_not_exist.append(store_id)
    if store_not_exist:
        print(f"Stores {', '.join(store_not_exist)} not found.")

if __name__ == '__main__':
    main()