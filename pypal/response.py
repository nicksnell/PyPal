"""PayPal API Response"""

from cgi import parse_qs

class PayPalResponse(object):
	
	def __init__(self, raw_response):
		self.raw = raw_response
		self.args = parse_qs(raw_response)
		
	def __unicode__(self):
		return u'<PayPalResponse: %s>' % unicode(self.raw)
	
	def __str__(self):
		return str(self.__unicode__())
	
	def __getattr__(self, key):
		key = key.upper()
		
		try:
			value = self.args[key]
			
			if len(value) == 1:
				return value[0]
			
			return value
			
		except KeyError:
			raise AttributeError(self)
	
	@property
	def status(self):
		return self.ack.upper()
	
	@property
	def success(self):
		return self.status in ['SUCCESS', 'SUCCESSWITHWARNING']
		
	@property
	def error_msg(self):
		return self.l_longmessage0
		
	@property
	def error_code(self):
		return self.l_errorcode0