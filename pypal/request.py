"""PayPal API Requests"""

import urllib
from socket import gethostname

class PayPalRequest(object):
	"""Object representation of a PayPal API request"""
	
	def __init__(self, url, data=None, headers={}):
		"""Setup the request"""
		
		self.headers = {
			'Host': gethostname(),
			'User-Agent': 'Python/PayPalAPI',
			'Content-Type': 'text/namevalue', # @@ 'text/xml',
			'Connection': 'close',
		}
		
		self.url = url
		
		# Setup data
		self._data = {}
		
		if data:
			self.set_data(data)
		
		for key, value in headers.items():
			self.add_header(key, value)
			
	def __unicode__(self):
		return u'<PayPalRequest: %s>' % self.get_data()
		
	def __str__(self):
		return str(self.__unicode__())
		
	def __repr__(self):
		return self.__str__()
		
	def add_header(self, key, val):
		self.headers[key.capitalize()] = val
		
	def has_header(self, header_name):
		return True if header_name in self.headers else False
		
	def get_header(self, header_name, default=None):
		return self.headers.get(header_name, default)
		
	def add_data(self, data):
		self._data.update(data)
	
	def get_data(self):
		return urllib.urlencode(self._data)
	
	def set_data(self, data):
		self._data = data
		
	data = property(get_data, set_data)
	
	def get_length(self):
		return len(self.data)
	