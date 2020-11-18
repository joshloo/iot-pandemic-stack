# importing the requests library 
import requests 

# api-endpoint 
URL = "http://127.0.0.1:5000/api/users"

# sending get request and saving the response as response object 
r = requests.get(url = URL) 
  
# extracting data in json format 
data = r.json() 
  
# extracting username, ID, temperature
username 	= data['username']
ID 		= data['ID']
temperature 	= data['temperature']
  
# printing the output 
print("User:%s\nID:%s\nTemperature:%s Celsius"
      %(username, IC,temperature)) 