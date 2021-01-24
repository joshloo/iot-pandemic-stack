# importing the requests library 
import requests 
import random

# defining the api-endpoint  
API_ENDPOINT = "http://127.0.0.1:5000/api/users"

for x in range(100):
    # data to be sent to api 
    data = {'username': 'Josh Loo',
            'IC':       '010101-01-0101',
            'temperature':  str(random.randint(1,999)) + '.' + str(random.randint(1,999)),
            'location': 'long: 123,lat: 456',} 
      
    # sending post request and saving response as response object 
    r = requests.post(url = API_ENDPOINT, json = data) 
      
    # extracting response text  
    pastebin_url = r.text 
    print("The pastebin URL is:%s"%pastebin_url) 
