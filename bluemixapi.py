import requests
import base64

class BluemixAPI:

  def __init__(self, region_key, apiKey):
   
    self.access_token = ''
    self.refresh_token = ''
    self.region_keys = ['ng', 'eu-gb']
    self.region_key = ''
    self.apiKey = ''

    self.region_key = region_key
    self.apiKey = apiKey
    self.fetch_token()

  def fetch_token(self):
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded', 
      'Accept': 'application/json',
      'Authorization': 'Basic ' + base64.b64encode('bx:bx')}

    data='apikey=%s&grant_type=urn:ibm:params:oauth:grant-type:apikey&response_type=cloud_iam,uaa&uaa_client_id=cf&uaa_client_secret=' % self.apiKey
    
    url = 'https://iam.%s.bluemix.net/oidc/token' % self.region_key
    
    r = requests.post(url, data=data, headers=headers)
    
    if r.status_code == 200:
      self.access_token = r.json()['uaa_token']
      self.refresh_token = r.json()['uaa_refresh_token']
    else:
      print r.text
  
  def get_token(self):
    if self.access_token == '':
      self.fetch_token()
      
    return self.access_token
