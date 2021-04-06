import requests as req
#from xml.etree.ElementTree import fromstring, ElementTree as ET
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
    store_list = []
    for store_tag in soup.find_all('localstore'):
        for store_id in store_id_list:
            if store_tag.attrs['bucode'] == store_id:
                store_list.append(store_tag)
                store_id_list.remove(store_id)
    if store_id_list:
        for store_id in store_id_list:
            print(f"Store {store_id} was not found.")

def get_all_stores(soup):
    for store_tag in soup.find_all('localstore'):
        store = {}
        store['_id'] = store_tag.attrs['bucode']

    for stock_tag in soup.find_all('stock'):
        print()
        print(list(stock_tag))

def main():
    BASE_URL = "https://www.ikea.com/us/en/iows/catalog/availability/"

    args = sys.argv[1:]
    check_valid_args_syntax(args)

    product_code = args[0]

    r = req.get(BASE_URL + product_code)
    soup = BS(r.text, 'lxml')

    store_id_list = args[1:]
    if not store_id_list:
        get_all_stores(soup)
    else:
        get_select_stores(soup, store_id_list)

    r.close()

if __name__ == '__main__':
    main()

'''
tree = ET(fromstring(r.text))
root = tree.getroot()

header = root[0]
action_response = root[1]
availability = root[2]

stores = availability.findall('localStore')
for store in stores:
    for elem in store.iter():
        print(elem)
'''