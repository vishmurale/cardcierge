from urllib.parse import urlparse
from .categories import categories

# utility tools to infer category given url 
mappings = {
    'aa' : "airline",
    'delta' : "airline",
    'southwest' : "airline",
    'united' : "airline",
    'bestbuy': 'best_buy',
    'avis' : 'car_rental',
    'ikea' : 'furnishings',
    'homedepot' : 'home_improvement'
}

def get_store_name(url):
    '''
    Given a url, return the name of the merchant
    '''
    return urlparse(url).netloc.split('.')[-2].lower()

def _get_category(store_name):
    '''
    Given a store name, return the category, which must be in categories
    '''
    print(store_name)
    if store_name in categories:
        return store_name
    if store_name in mappings.keys():
        return mappings[store_name]
    return "other"
    
def get_category(url):
    '''
    Given url, return category
    '''
    return _get_category(get_store_name(url))
