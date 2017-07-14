import requests
class WASaaSAPI:

  def __init__(self, region_key, org, space, si_name = '', token = '', refresh_token = ''):    
    self.token = token
    self.si_name = si_name
    self.sid = ''
    self.adminip = ''
    self.wsadmin_user = ''
    self.wsadmin_pass = ''
    self.vpnConfig_link = ''
    self.space = space
    self.org = org
    self.regionKey = region_key
    # Available Environments:
    # Dallas - https://wasaas-broker.ng.bluemix.net/wasaas-broker/api/v1
    # London - https://wasaas-broker.eu-gb.bluemix.net/wasaas-broker/api/v1
    # Sydney - https://wasaas-broker.au-syd.bluemix.net/wasaas-broker/api/v1
    regions = {
      'ng': 'https://wasaas-broker.ng.bluemix.net/wasaas-broker/api/v1',
      'eu-gb': 'https://wasaas-broker.eu-gb.bluemix.net/wasaas-broker/api/v1',
      'au-syd': 'https://wasaas-broker.au-syd.bluemix.net/wasaas-broker/api/v1'
    }
    self.baseUrl = regions[self.regionKey]
    self._headers={
      'authorization': self.token,
      'Accept': 'application/json'
    }

  def get_vpnConfig_zip(self):
    if self.sid == '':
      self.fetch_resource_details()
    
    url = self.baseUrl + '/organizations/%s/spaces/%s/serviceinstances/%s/vpnconfig' % (self.org, self.space, self.sid)
    r = requests.get(url, headers=self._headers)
    if r.status_code != 200:
      print 'Error retrieving service instance vpn configuration. '
      print 'Server returned status code: %s' % r.status_code
      print r.text
      return False   
    
    return r.json()['VpnConfig']
    
  def get_wsadmin_user(self):
    if self.wsadmin_user == '':
      self.fetch_resource_details()
    return self.wsadmin_user

  def get_wsadmin_password(self):
    if self.wsadmin_pass == '':
      self.fetch_resource_details()
    return self.wsadmin_pass

  def get_adminip(self):
    if self.adminip == '':
      self.fetch_resource_details()

    return self.adminip
  
  def get_rootpassword(self):
    if self.rootpassword == '':
      self.fetch_resource_details()
    
    return self.rootpassword

  def fetch_resource_details(self):

    if self.sid == '':
      sis = self.get_serviceinstances(self.org, self.space)
      for s in sis:
        if s['ServiceInstance']['Name'] == self.si_name:
          si = s
          break
      
      if not si:
        print "Could not find service instance with name %s " % self.si_name
        return False

      # Ensure this is basic WAS as we don't support ND cluster yet
      if si['ServiceInstance']['ServiceType'] != 'WASBase':
        print "Don't support the service instance type %s " % si['ServiceInstance']['ServiceType']
        return False
      
      self.sid = si['ServiceInstance']['ServiceInstanceID']

    url = self.baseUrl + '/organizations/%s/spaces/%s/serviceinstances/%s/resources' % (self.org, self.space, self.sid)
    r = requests.get(url, headers=self._headers)
    if r.status_code != 200:
      print 'Error retrieving service instances. '
      print 'Server returned status code: %s' % r.status_code
      print r.text
      return False   

    self.adminip        = r.json()[0]['osHostname']
    self.rootpassword   = r.json()[0]['osAdminPassword']
    self.wsadmin_user   = r.json()[0]['wasAdminUser']
    self.wsadmin_pass   = r.json()[0]['wasAdminPass']
    self.vpnConfig_link = r.json()[0]['vpnConfigLink']

    return True

  def get_resource_details(self, resourceid, serviceinstanceid, space, organisation):

    url = baseUrl + '/organizations/%s/spaces/%s/serviceinstances/%s/resources/%s' % (organisation, space, serviceinstanceid, resourceid)
    r = requests.get(url, headers=self._headers)
    return r.json()

  def get_serviceinstances(self, organisation, space):

    url = self.baseUrl + '/organizations/%s/spaces/%s/serviceinstances' % (organisation, space)
    r = requests.get(url, headers=self._headers)

    if r.status_code != 200:
      print 'Error retrieving service instances. '
      print 'Server returned status code: %s' % r.status_code
      print r.text
      return False
    return r.json()
      
  def get_spaces(self, organisation):

    url = baseUrl + '/organizations/%s/spaces' % (organisation)
    r = requests.get(url, headers=self._headers)
    return r.json()
      
  def get_serviceinstance_id(self, organisation, space, serviceinstance_name):
    serviceinstances = self.get_serviceinstances(organisation, space)    
    for si in serviceinstances:
      if si['ServiceInstance']['Name'] == serviceinstance_name:
        return si['ServiceInstance']['ServiceInstanceID']
      
    print "Could not find service instance " + serviceinstance_name
    return False
      
  def get__resource_from_id(self,organisation, space, sid):
    url = baseUrl + '/organizations/%s/spaces/%s/serviceinstances/%s/resources' % (organisation, space, sid)

  def get_serviceinstance_details(self, organisation, space, serviceinstance_name):

    sis = self.get_serviceinstances(organisation, space)
    for s in sis:
      if s['ServiceInstance']['Name'] == serviceinstance_name:
        si = s
        break
              
    if not serviceinstance:
      print "Could not find service instance with name %s " % serviceinstance_name
      return False
          
    # Ensure this is basic WAS as we don't support ND cluster yet
    if si['ServiceInstance']['ServiceType'] != 'WASBase':
      print "Don't support the service instance type %s " % si['ServiceInstance']['ServiceType']
      return False
    


      

