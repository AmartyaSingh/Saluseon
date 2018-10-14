# importing basic modules
import requests
import json
  
# api-endpoint 
URL = "<<server url>>"
  
# generating data here for demo purposes 
feat = list(range(24))
s_id = 1

#creating a json object
PARAMS = json.dumps({s_id:{'feat':feat}})
  
# defining a params dict for the parameters to be sent to the API 
header_list = {'content-type':'application/json', 'data':PARAMS}
  
# sending get request and saving the response as response object 
r = requests.post(url = URL, headers = header_list)
 
#response code
print(r)
