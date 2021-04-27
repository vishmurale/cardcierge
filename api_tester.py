#!/usr/bin/env python3
import json 
import requests

DEBUG = True
TOKEN = "2e31bf48bce375761dfad9b1526a0908cdbf46f5" #set a token for use
def print_data(response):
	response_dict = json.loads(response.text)
	tok = None 
	if isinstance(response_dict, list):
		for i in response_dict:
			print(i)
			
		return 
	
	for i in response_dict:
		print(i, ":", response_dict[i])
	
base_url = "https://cardcierge.herokuapp.com/" if not DEBUG else "http://127.0.0.1:8000/"
	
##admin user example	to init database
# url = base_url +'token/obtain'
# data = {'username': 'vmurale', "password":"123"} #NEED TO USE ADMIN ACCOUNT
# print_data(requests.post(url, data = data))
# url = base_url+'init_database'
# headers = {'Authorization': 'Token 9bd33a7144115d572570a3f2472c20b6e32661df'} #Replace token
# data = {}
# print(requests.get(url, headers=headers, data = data))
	
##Example of registering a user...
# url = base_url+'account/register'
# data = {'username': 'vm373', "password":"itlit"}
# print_data(requests.post(url, data = data))

#Example of getting token for user 
# url = base_url +'token/obtain'
# data = {'username': 'jaredtruong', "password":"admin"}
# print_data(requests.post(url, data = data))

# #Example of inferring catogery 
# url = base_url + "infercategory"
# data = {"url" : "https://www.bestbuy.com/site/insignia-5-qt-digital-air-fryer-stainless-steel/6351671.p?skuId=6351671"}
# headers = {'Authorization': 'Token {0}'.format("a4f37e20746f8f9d0e5f8910bed75848507f0917")}
# print_data(requests.post(url, headers=headers, data = data))

##creating a credit card for a user 
# url = base_url + 'creditcards/'
# headers = {'Authorization': 'Token {0}'.format(TOKEN)}
# data = {'card_number': '22222', "expiration":"7/28", "security_code":"123", "card_type":"1"}
# #Notice for card_type, we pass a number, this is the primary key of the credit card type in the data base
# print_data(requests.post(url, headers=headers, data = data))

##getting all credit cards assoicated with user 
# url = base_url + 'creditcards/'
# headers = {'Authorization': 'Token {0}'.format(TOKEN)}
# print_data(requests.get(url, headers=headers))

##updating a credit card 
# url = base_url + 'creditcards/2/'
# headers = {'Authorization': 'Token {0}'.format(TOKEN)}
# data = {"expiration":"8/29"}
# #Notice for card_type, we pass a number, this is the primary key of the credit card type in the data base
# print_data(requests.patch(url, headers=headers, data = data))

##deleting a credit card 
#url = base_url + 'creditcards/1/'
# headers = {'Authorization': 'Token {0}'.format(TOKEN)}
##Notice for card_type, we pass a number, this is the primary key of the credit card type in the data base
#requests.delete(url, headers=headers)

##get all categories
#url = base_url + 'categories/'
# headers = {'Authorization': 'Token {0}'.format(TOKEN)}
#print_data(requests.get(url, headers=headers))

##get all credit card types 
#url = base_url + 'credit_types/'
# headers = {'Authorization': 'Token {0}'.format(TOKEN)}
#print_data(requests.get(url, headers=headers))

#get specific type info from credit card 
#url = base_url + 'credit_types/2'
# headers = {'Authorization': 'Token {0}'.format(TOKEN)}
#print_data(requests.get(url, headers=headers))

#get encryption key 
# url = base_url + 'getusersettings'
# headers = {'Authorization': 'Token {0}'.format(TOKEN)}
# print_data(requests.get(url, headers=headers))


#given a category return the best credit card 
# we can find a list of all possible categories in categories.py
# url = base_url + 'getbestcard'
# headers = {'Authorization': 'Token {0}'.format(TOKEN)}
# data = {"category":"airbnb"}
# print_data(requests.post(url, headers=headers, data=data))


"""
Below are above variants related to sign up bonuses 
"""


# #creating a credit card for a user with a sign up bonus
# url = base_url + 'creditcards/'
# headers = {'Authorization': 'Token {0}'.format(TOKEN)}
# data = {'card_number': '1234567890', "expiration":"7/29", "security_code":"123", "card_type":"2", "welcome_offer":"1", "open_date":"2021-03-01", "reward_value_override":"2.0"}
# # note for card_type and welcome_offer, we pass a number, this is the primary key of the credit card type in the data base
# # note that welcome_offer, open_date, and reward_value_override are optional fields
# print_data(requests.post(url, headers=headers, data = data))

# # getting all possible subs
# url = base_url + 'subs/'
# headers = {'Authorization': 'Token {0}'.format(TOKEN)}
# print_data(requests.get(url, headers=headers))

# #updating a credit card to have welcome offer
# url = base_url + 'creditcards/1/'
# headers = {'Authorization': 'Token {0}'.format(TOKEN)}
# data = {"expiration":"8/29", "welcome_offer":"2"}
# #Notice for card_type, we pass a number, this is the primary key of the credit card type in the data base
# print_data(requests.patch(url, headers=headers, data = data))

