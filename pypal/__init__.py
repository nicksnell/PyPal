"""PayPal API"""

import urllib
import urllib2
import string

# Import related libs
from exceptions import *
from paymentrequest import *
from request import *
from response import *
from settings import *

__all__ = ('PayPalAPI',)

PAYPAL_API_VERSION = '63.0'
PAYPAL_MODE_LIVE = 1
PAYPAL_MODE_SANDBOX = 2

class PayPalAPI(object):
	
	def __init__(self, user, passwd, signature, mode=PAYPAL_MODE_SANDBOX, locale=u'US', attempts=2, debug=False):
		self.user = user
		self.passwd = passwd
		self.signature = signature
		
		self.locale = locale
		self.mode = mode
		self.request_attempts = attempts
		
		self.debug = debug
		
		self._token = None
		
		self.last_request = None
		self.last_response = None
		
		if self.mode == PAYPAL_MODE_LIVE:
			self.endpont = u'https://api-3t.paypal.com/nvp'
			self.url = u'https://www.paypal.com/webscr?cmd=_express-checkout&token=%s'
		elif self.mode == PAYPAL_MODE_SANDBOX:
			self.endpont = u'https://api-3t.sandbox.paypal.com/nvp'
			self.url = u'https://www.sandbox.paypal.com/webscr?cmd=_express-checkout&token=%s'
		
	def set_token(self, token):
		self._token = token
		
	def get_token(self):
		return self._token
		
	token = property(get_token, set_token)
	
	def _build_request(self, method):
		return PayPalRequest(self.endpont, self.user, self.passwd, self.signature, PAYPAL_API_VERSION, method)
		
	def _call(self, request):
		"""Call PayPal API"""
		
		request.add_header('Content-Length', request.get_length())
		
		attempt = 1
		last_error = ''
		
		# We must make a urllib request here
		req = urllib2.Request(request.url, request.data)
		
		while attempt < self.request_attempts:
			try:
				response = urllib2.urlopen(req)
			except urllib2.HTTPError, e:
				# Server didnt give us 200, we can try again if we have 
				# attempts left
				attempt += 1
				last_error = 'HTTP error: %s' % e.code
			
			except urllib2.URLError, e:
				# Cant reach the server, we can try again if we have 
				# attempts left
				attempt += 1
				last_error = 'URL error: %s' % e.reason
			
			else:
				break
		else:
			# We have exhaused the attempts
			if self.debug:
				raise PayPalCallError('Unable to connect to PayPal, tried %s times, The last error was "%s", Data was "%s", URL was "%s"' % (attempt, last_error, request.data, request.url))
			else:
				raise PayPalCallError('Unable to connect to PayPal, The last error was "%s"' % last_error)
			
		# We have a response 
		response_data = response.read()
		
		return PayPalResponse(response_data)
		
	def set_express_checkout(self, items, payment, return_url, cancel_url, callback=u'', callback_timeout=u'', email=u'', 
							shipping=None, shipping_confirm=False, shipping_allow_note=False, shipping_allow_overide=False, 
							brand_name=u'', landing_page=u'Login', soultion_type=u'Sole', color=u'ffffff', page_style=u'', logo=u'', 
							token=None, **kwargs):
		"""Run the SetExpressCheckout API method - returns URL to PayPal express checkout on success"""
		
		request = self._build_request(u'SetExpressCheckout')
		
		set_express_checkout_data = {
			'TOKEN': token or self.token or u'',
			'LOCALECODE': self.locale,
			
			# URL details
			'RETURNURL': return_url,
			'CANCELURL': cancel_url,
			'CALLBACK': callback,
			'CALLBACKTIMEOUT': callback_timeout,
			
			# User & order details
			'EMAIL': email,
			
			# Interface styling
			'BRANDNAME': brand_name,
			'LANDINGPAGE': landing_page,
			'SOLUTIONTYPE': soultion_type,
			'PAYFLOWCOLOR': color,
			'PAGESTYLE': page_style,
			'HDRIMG': logo
		}
		
		request.add_data(set_express_checkout_data)
		
		# Add the items to our request
		for index, item in enumerate(items):
			item.item_number = index
			request.add_data(item.get_data())
		
		# Add the payment details to the request
		request.add_data(payment.get_data())
		
		# Add shipping information?
		if shipping:
			shipping_data = {
				# Shipping details
				'REQCONFIRMSHIPPING': '1' if shipping_confirm else '0', # 0 or 1
				'NOSHIPPING': shipping, # 0, 1 or 2
				'ALLOWNOTE': '1' if shipping_allow_note else '0', # 0 or 1
				'ADDROVERRIDE': '1' if shipping_allow_overide else '0', # 0 or 1
			}
			
			request.add_data(shipping_data)
			request.add_data(shipping.get_data())
		
		# Custom data
		if kwargs:
			extra_args = [(k.upper(), v) for k, v in kwargs.items()]
			request.add_data(dict(extra_args))
		
		if self.debug:
			print request
		
		self.last_request = request
		
		try:
			response = self._call(request)
		except PayPalCallError, e:
			raise PayPalExpressCheckoutError(u'Unable to reach PayPal: %s' % e)
		
		if self.debug:
			print response
		
		self.last_response = response
		
		if not response.success:
			raise PayPalExpressCheckoutError(u'PayPal Error: %s %s' % (response.status, response.error_msg))
		
		self.token = response.token
		
		return self.url % self.token
	
	def get_express_checkout_details(self, token=None):
		"""Run the GetExpressCheckoutDetails API method - returns the current express checkout token on success"""
		
		request = self._build_request(u'GetExpressCheckoutDetails')
		
		get_express_checkout_details_data = {
			'TOKEN': token or self.token or u'',
		}
		
		request.add_data(get_express_checkout_details_data)
		
		if self.debug:
			print request
		
		self.last_request = request
		
		try:
			response = self._call(request)
		except PayPalCallError, e:
			raise PayPalExpressCheckoutError(u'Unable to reach PayPal: %s' % e)
		
		if self.debug:
			print response
		
		self.last_response = response
		
		if not response.success:
			raise PayPalExpressCheckoutError(u'PayPal Error: %s %s' % (response.status, response.error_msg))
		
		self.token = response.token
		
		return response.payerid
		
	def do_express_checkout_payment(self, payerid, items=None, payment=None, shipping=None, token=None, **kwargs):
		"""Run the GetExpressCheckoutDetails API method - returns the current express checkout token on success"""
		
		request = self._build_request(u'DoExpressCheckoutPayment')
		
		do_express_checkout_details_data = {
			'TOKEN': token or self.token or u'',
			'PAYERID': payerid,
		}
		
		request.add_data(do_express_checkout_details_data)
		
		# Add the items to our request
		if items:
			for index, item in enumerate(items):
				item.item_number = index
				request.add_data(item.get_data())
		
		# Add the payment details to the request
		if payment:
			request.add_data(payment.get_data())
		
		# Add shipping information?
		if shipping:
			request.add_data(shipping.get_data())
		
		# Custom data
		if kwargs:
			extra_args = [(k.upper(), v) for k, v in kwargs.items()]
			request.add_data(dict(extra_args))
			
		if self.debug:
			print request
		
		self.last_request = request
		
		try:
			response = self._call(request)
		except PayPalCallError, e:
			raise PayPalExpressCheckoutError(u'Unable to reach PayPal: %s' % e)
			
		if self.debug:
			print response
		
		self.last_response = response
		
		if not response.success:
			raise PayPalExpressCheckoutError(u'PayPal Error: %s %s' % (response.status, response.error_msg))
			
		return response