import unittest
from .. import design_and_response
import pandas
import numpy as np


class TestDesignResponse(unittest.TestCase):

	def test_nothing(self):
		meta = pandas.DataFrame()
		meta['isTs']=[True, True, True, True, False]
  		meta['is1stLast'] = ['f','m','m','l','e']
  		meta['prevCol'] = ['NA','ts1','ts2','ts3', 'NA']
  		meta['del_t'] = ['NA', 1, 2, 5, 'NA']
  		meta['condName'] = ['ts1','ts2','ts3','ts4','ss']
  		exp = pandas.DataFrame(np.reshape(range(10), (2,5)) + 1,
  		 index = ['gene' + str(i + 1) for i in range(2)],
  		 columns = ['ts' + str(i + 1) for i in range(4)] + ['ss'])
  		print meta
  		ds, resp = design_and_response.Legacy_Design_Response_Driver().get_design_response(exp, meta)
		self.assertTrue(False)


	def test_num_columns_design_response(self):
		self.assertTrue(False)



