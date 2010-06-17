"""PayPal API Exceptions"""

class PayPalGenericError(Exception):
	pass
	
class PayPalCallError(PayPalGenericError):
	pass
	
class PayPalExpressCheckoutError(PayPalGenericError):
	pass
