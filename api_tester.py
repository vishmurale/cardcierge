#!/usr/bin/env python3
import json 
import requests

DEBUG = True
TOKEN = "b4adbf9e7e787abda661df58fca36b7c79ddcb34" #set a token for use
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
#url = base_url +'token/obtain'
#data = {'username': 'ENTERADMINUSER', "password":"ENTERPASSWORD"} #NEED TO USE ADMIN ACCOUNT
#print_data(requests.post(url, data = data))
#url = base_url+'init_database'
#headers = {'Authorization': 'Token bc0acdc2f6c8d389e54eab5db3bb47661ed6fcd0'} #Replace token
#data = {}
#print_data(requests.get(url, headers=headers, data = data))
	
##Example of registering a user...
# url = base_url+'account/register'
# data = {'username': 'vm373', "password":"itlit"}
# print_data(requests.post(url, data = data))

##Example of getting token for user 
# url = base_url +'token/obtain'
# data = {'username': 'vm373', "password":"itlit"}
# print_data(requests.post(url, data = data))

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

##given a category return the best credit card 
#url = base_url + 'getbestcard'
# headers = {'Authorization': 'Token {0}'.format(TOKEN)}
#data = {"category":"Travel"}
#print_data(requests.post(url, headers=headers, data=data))

#get encryption key 
url = base_url + 'getusersettings'
headers = {'Authorization': 'Token {0}'.format(TOKEN)}
print_data(requests.get(url, headers=headers))