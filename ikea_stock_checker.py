import requests as req
from bs4 import BeautifulSoup as BS
import sys

def execution_help():
    print("Arguments: <required 8-digit product code> <optional 3-digit store code(s)> ...")
    print("No store code argument(s) will return product availability results for all US stores.")
    print("Only 1 product may be requested at once.")
    exit()

def check_valid_args_syntax(args):
    if len(args[0]) != 8:
        execution_help()
    for code in args[1:]:
        if len(code) != 3:
            execution_help()

def get_select_stores(soup, store_id_list):
    stores = []
    for store_tag in soup.find_all('localstore'):
        for store_id in store_id_list:
            if store_tag.attrs['bucode'] == store_id:
                store_list.append(store_tag)
                store_id_list.remove(store_id)
    if store_id_list:
        for store_id in store_id_list:
            print(f"Store {store_id} was not found.")

    return stores

def get_all_stores(soup):
    stores = []

    for store_tag in soup.find_all('localstore'):
        store = {}

        store['store_id'] = int(store_tag.attrs['bucode'])
        store['available_stock'] = int(store_tag.find('availablestock').contents[0])
        store['in_stock_probability'] = store_tag.find('instockprobabilitycode').contents[0]

        restock_date = store_tag.find('restockdate')
        if restock_date is not None:
            store['restock_date'] = restock_date.contents[0]
        else:
            store['restock_date'] = None

        four_forecasts = {}
        forecast = store_tag.find('forecasts').contents
        i = 1
        for fc in forecast:
            date = fc.find('validdate').contents[0]
            stock = fc.find('availablestock').contents[0]
            four_forecasts['forecast_date'] = date
            four_forecasts['forecast_stock'] = int(stock)
            key = ['forecast', str(i)]
            key_name = '_'.join(key)
            store[key_name] = four_forecasts
            i = i + 1

        stores.append(store)

    return stores

def main():
    BASE_URL = "https://www.ikea.com/us/en/iows/catalog/availability/"

    args = sys.argv[1:]
    check_valid_args_syntax(args)
    product_code = args[0]
    store_id_list = args[1:]

    r = req.get(BASE_URL + product_code)
    soup = BS(r.text, 'lxml')

    if not store_id_list:
        stores = get_all_stores(soup)
    else:
        stores = get_select_stores(soup, store_id_list)
    
    try:
        f = open("stores.txt", "w")
    except FileNotFoundError: 
        f = open("stores.txt", "x")
    f.write(str(stores))
    f.close()

    r.close()

if __name__ == '__main__':
    main()