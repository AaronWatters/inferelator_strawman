import unittest
from .. import design_and_response
import pandas
import numpy as np


class TestDesignResponse(unittest.TestCase):

	def setup(self):
		self.meta = pandas.DataFrame()
		self.meta['isTs']=[True, True, True, True, False]
  		self.meta['is1stLast'] = ['f','m','m','l','e']
  		self.meta['prevCol'] = ['NA','ts1','ts2','ts3', 'NA']
  		self.meta['del.t'] = ['NA', 1, 2, 5, 'NA']
  		self.meta['condName'] = ['ts1','ts2','ts3','ts4','ss']

  		self.exp = pandas.DataFrame(np.reshape(range(10), (2,5)) + 1,
  		 index = ['gene' + str(i + 1) for i in range(2)],
  		 columns = ['ts' + str(i + 1) for i in range(4)] + ['ss'])
  		delT_min = 2
		delT_max = 4
		self.tau = 2

  		return design_and_response.Legacy_Design_Response_Driver().get_design_response(self.exp, self.meta, delT_min, delT_max, self.tau)

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


	def test_response_matrix_steady_state(self):
		ds, resp = self.setup()
		self.assertEqual(list(resp['ts4']), list(self.exp['ts4']))
		self.assertEqual(list(resp['ss']), list(self.exp['ss']))

	def test_response_matrix_time_series(self):
		ds, resp = self.setup()
		expression_1 = np.array(list(self.exp['ts1']))
		expression_2 = np.array(list(self.exp['ts2']))
		expected_response_1 = expression_1 + self.tau * (expression_2 - expression_1) /  float(self.meta['del.t'][1])

		expression_3 = np.array(list(self.exp['ts3']))
		expected_response_2 = expression_2 + self.tau * (expression_3 - expression_2) /  float(self.meta['del.t'][2])

		self.assertEqual(list(resp['ts1']), list(expected_response_1))
		self.assertEqual(list(resp['ts2']), list(expected_response_2), 
			msg = 'In a time series the response should follow the formula for the expected_response_2')


