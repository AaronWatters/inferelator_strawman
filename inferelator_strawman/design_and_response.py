import pandas
import subprocess

class Legacy_Design_Response_Driver:

	def get_design_response(exp_mat, meta_data):
		exp_mat.to_csv('exp_mat.csv')
		meta_data.to_csv('meta_data.csv')
		subprocess.call(['R', '-f', './design_and_response_driver.R'])
		final_design = pandas.read_csv('design.tsv', sep='\t')
		final_response = pandas.read_csv('response.tsv', sep='\t')
		return (final_design, final_response)