import unittest
from .. import design_and_response
import pandas
import numpy as np


class TestDesignResponse(unittest.TestCase):

	def setup(self):
		meta = pandas.DataFrame()
		meta['isTs']=[True, True, True, True, False]
  		meta['is1stLast'] = ['f','m','m','l','e']
  		meta['prevCol'] = ['NA','ts1','ts2','ts3', 'NA']
  		meta['del.t'] = ['NA', 1, 2, 5, 'NA']
  		meta['condName'] = ['ts1','ts2','ts3','ts4','ss']

  		self.exp = pandas.DataFrame(np.reshape(range(10), (2,5)) + 1,
  		 index = ['gene' + str(i + 1) for i in range(2)],
  		 columns = ['ts' + str(i + 1) for i in range(4)] + ['ss'])
  		delT_min = 2
		delT_max = 4
		tau = 2

  		return design_and_response.Legacy_Design_Response_Driver().get_design_response(self.exp, meta, delT_min, delT_max, tau)

	def test_design_matrix(self):
		# Set up variables 

		ds, resp = self.setup()
  		print ds
  		print resp
  		self.assertEqual(ds.shape, (2, 4))
  		self.assertEqual(list(ds.columns), ['ts4', 'ss', 'ts1', 'ts2'], 
			msg = "Guarantee that the ts3 condition is dropped, since its delT of 5 is greater than delt_max of 4")
  		for col in ds:
  			self.assertEqual(list(ds[col]), list(self.exp[col]), 
  				msg = '{} column in the design matrix should be equal to that column in the expression matrix'.format(col))

		self.assertEqual(list(ds['ss']), [5, 10])
		self.assertEqual(list(ds['ss']), list(resp['ss']), msg = 'Steady State design and response should be equal')


	def test_response_matrix(self):
		ds, resp = self.setup()
		self.assertEqual(list(resp['ts4']), [4, 9])
		self.assertEqual(list(resp['ts2']), list(self.exp['ts3']))
		self.assertEqual(list(resp['ts1']), list(self.exp['ts2']), 
			msg = 'In a time series the response should be the expression data at time t + 1')


