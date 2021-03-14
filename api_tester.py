#!/usr/bin/env python3
import json 
import requests

DEBUG = True
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
	
#admin user example	to init database
# url = base_url +'token/obtain'
# data = {'username': 'jtruong', "password":"admin"} #NEED TO USE ADMIN ACCOUNT
# print_data(requests.post(url, data = data))
# url = base_url+'init_database'
# headers = {'Authorization': 'Token b2bb3fa6f42d2e9ddc7502d59b0f959bd0130e70'} #Replace token
# data = {}
# print(requests.get(url, headers=headers, data = data))
	
##Example of registering a user...
#url = base_url+'account/register'
#data = {'username': 'jared', "password":"123"}
#print_data(requests.post(url, data = data))

##Example of getting token for user 
#url = base_url +'token/obtain'
#data = {'username': 'vm373', "password":"itlit"}
#print_data(requests.post(url, data = data))

# #creating a credit card for a user 
# url = base_url + 'creditcards/'
# headers = {'Authorization': 'Token b2bb3fa6f42d2e9ddc7502d59b0f959bd0130e70'}
# data = {'card_number': '22222', "expiration":"7/28", "security_code":"123", "card_type":"2"}
# #Notice for card_type, we pass a number, this is the primary key of the credit card type in the data base
# print_data(requests.post(url, headers=headers, data = data))

# #creating a credit card for a user with a sign up bonus
# url = base_url + 'creditcards/'
# headers = {'Authorization': 'Token b2bb3fa6f42d2e9ddc7502d59b0f959bd0130e70'}
# data = {'card_number': '1234567890', "expiration":"7/29", "security_code":"123", "card_type":"2", "welcome_offer":"1", "open_date":"2021-03-01", "reward_value_override":"2.0"}
# # note for card_type and welcome_offer, we pass a number, this is the primary key of the credit card type in the data base
# # note that welcome_offer, open_date, and reward_value_override are optional fields
# print_data(requests.post(url, headers=headers, data = data))

# # getting all possible subs
# url = base_url + 'subs/'
# headers = {'Authorization': 'Token b2bb3fa6f42d2e9ddc7502d59b0f959bd0130e70'}
# print_data(requests.get(url, headers=headers))

# #getting all credit cards assoicated with user 
# url = base_url + 'creditcards/'
# headers = {'Authorization': 'Token b2bb3fa6f42d2e9ddc7502d59b0f959bd0130e70'}
# print_data(requests.get(url, headers=headers))

# #updating a credit card 
# url = base_url + 'creditcards/1/'
# headers = {'Authorization': 'Token b2bb3fa6f42d2e9ddc7502d59b0f959bd0130e70'}
# data = {"expiration":"8/29", "welcome_offer":"2"}
# #Notice for card_type, we pass a number, this is the primary key of the credit card type in the data base
# print_data(requests.patch(url, headers=headers, data = data))

# #deleting a credit card 
# url = base_url + 'creditcards/1/'
# headers = {'Authorization': 'Token b2bb3fa6f42d2e9ddc7502d59b0f959bd0130e70'}
# #Notice for card_type, we pass a number, this is the primary key of the credit card type in the data base
# requests.delete(url, headers=headers)

# #get all categories
# url = base_url + 'categories/'
# headers = {'Authorization': 'Token b2bb3fa6f42d2e9ddc7502d59b0f959bd0130e70'}
# print_data(requests.get(url, headers=headers))

# #get all credit card types 
# url = base_url + 'credit_types/'
# headers = {'Authorization': 'Token b2bb3fa6f42d2e9ddc7502d59b0f959bd0130e70'}
# print_data(requests.get(url, headers=headers))

#get specific type info from credit card 
#url = base_url + 'credit_types/2'
#headers = {'Authorization': 'Token b2bb3fa6f42d2e9ddc7502d59b0f959bd0130e70'}
#print_data(requests.get(url, headers=headers))

# #given a category return the best credit card 
# # we can find a list of all possible categories in categories.py
# url = base_url + 'getbestcard'
# headers = {'Authorization': 'Token b2bb3fa6f42d2e9ddc7502d59b0f959bd0130e70'}
# data = {"category":"airbnb"}
# print_data(requests.post(url, headers=headers, data=data))
