"""Payment Request Objects"""

__all__ = ('PaymentRequest', 'PaymentRequestItem', 'PaymentRequestShippingAddress', 'PaymentRequestPayment')

class PaymentRequest(object):
	
	def __init__(self, *args, **kwargs):
		if 'request_id' in kwargs:
			self._request_id = kwargs['request_id']
			del kwargs['request_id']
		else:
			self._request_id = 0
		
		self._item_number = None
		
	def _get_data(self, base={}):
		data = {}
		
		for key, value in base.items():
			prefix = ''
			
			if self.item_number is not None:
				prefix = 'L_'
			
			data['%sPAYMENTREQUEST_%s_%s' % (prefix, self.request_id, key)] = value
			
		return data
	
	def get_data(self):
		raise NotImplementedError
		
	def get_item_number(self):
		return self._item_number
		
	def set_item_number(self, v):
		self._item_number = v
		
	item_number = property(get_item_number, set_item_number)
	
	def get_request_id(self):
		return self._request_id
		
	def set_request_id(self, v):
		self._request_id = v
		
	request_id = property(get_request_id, set_request_id)
	
class PaymentRequestItem(PaymentRequest):

	def __init__(self, name, description, amt, quantity, number=None, tax=None, url=None, *args, **kwargs):
		# @@ Add support for ITEMWEIGHTVALUE, ITEMLENGTHVALUE, ITEMWIDTHVALUE, ITEMHEIGHTVALUE
		
		super(PaymentRequestItem, self).__init__(*args, **kwargs)
		
		if 'item_number' in kwargs:
			self._item_number = kwargs['item_number']
			del kwargs['item_number']
		else:
			self._item_number = None
		
		self.name = name
		self.description = description
		self.amt = str(amt) if amt else ''
		self.quantity = str(quantity) if quantity else ''
		self.number = str(number) if number else ''
		self.tax = str(tax) if tax else ''
		self.url = url
	
	def get_data(self):
		item_data = {
			'NAME%s' % self.item_number: self.name or '',
			'DESC%s' % self.item_number: self.description or '',
			'AMT%s' % self.item_number: self.amt or '',
			'NUMBER%s' % self.item_number: self.number or '',
			'QTY%s' % self.item_number: self.quantity or '',
			'TAXAMT%s' % self.item_number: self.tax or '',
			'ITEMURL%s' % self.item_number: self.url or ''
		}
		
		return self._get_data(base=item_data)

class PaymentRequestShippingAddress(PaymentRequest):
	
	def __init__(self, name, street, city, state, postal_zip, country, street_2=u'', phone_number=u'', *args, **kwargs):
		
		super(PaymentRequestShippingAddress, self).__init__(*args, **kwargs)
		
		self.name = name
		self.street = street
		self.street_2 = street_2
		self.city = city
		self.state = state
		self.postal_zip = postal_zip
		self.country = country
		self.phone_number = phone_number
		
	def get_data(self):
		item_data = {
			'SHIPTONAME': self.name,
			'SHIPTOSTREET': self.street,
			'SHIPTOSTREET2': self.street_2,
			'SHIPTOCITY': self.city,
			'SHIPTOSTATE': self.state,
			'SHIPTOZIP': self.postal_zip,
			'SHIPTOCOUNTRY': self.country,
			'SHIPTOPHONENUM': self.phone_number,
		}
		
		return self._get_data(base=item_data)
		
class PaymentRequestPayment(PaymentRequest):
	
	def __init__(self, amt, currency=u'USD', itemamt=u'', shippingamt=u'', insuranceamt=u'', shipdiscamt=u'',
				insuranceoffered=u'', handlingamt=u'', taxamt=u'', desc=u'', custom=u'', invnum=u'', notifyurl=u'',
				notetext=u'', transactionid=u'', allowedpaymentmethod=u'', paymentaction=u'Sale', paymentrequestid=u'',
				*args, **kwargs):
				
		super(PaymentRequestPayment, self).__init__(*args, **kwargs)
		
		self.amt = amt
		self.currency = currency
		self.itemamt = itemamt
		self.shippingamt = shippingamt
		self.insuranceamt = insuranceamt
		self.shipdiscamt = shipdiscamt
		self.insuranceoffered = insuranceoffered
		self.handlingamt = handlingamt
		self.taxamt = taxamt
		self.desc = desc
		self.custom = custom
		self.invnum = invnum
		self.notifyurl = notifyurl
		self.notetext = notetext
		self.transactionid = transactionid
		self.allowedpaymentmethod = allowedpaymentmethod
		self.paymentaction = paymentaction
		self.paymentrequestid = paymentrequestid
		
	def get_data(self):
		item_data = {
			'AMT': self.amt,
			'CURRENCYCODE': self.currency,
			'ITEMAMT': self.itemamt,
			'SHIPPINGAMT': self.shippingamt,
			'INSURANCEAMT': self.insuranceamt,
			'SHIPDISCAMT': self.shipdiscamt,
			'INSURANCEOFFERED': self.insuranceoffered,
			'HANDLINGAMT': self.handlingamt,
			'TAXAMT': self.taxamt,
			'DESC': self.desc,
			'CUSTOM': self.custom,
			'INVNUM': self.invnum,
			'NOTIFYURL': self.notifyurl,
			'NOTETEXT': self.notetext,
			'TRANSACTIONID': self.transactionid,
			'ALLOWEDPAYMENTMETHOD': self.allowedpaymentmethod,
			'PAYMENTACTION': self.paymentaction,
			'PAYMENTREQUESTID': self.paymentrequestid,
		}
		
		return self._get_data(base=item_data)