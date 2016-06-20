import pandas
import subprocess
import os

class Legacy_Design_Response_Driver:

	def get_design_response(self, exp_mat, meta_data):
		# Change the current working directory
		cwd = os.getcwd()
		new_dir = os.path.dirname(os.path.abspath(__file__))
		os.chdir(new_dir)
		self.convert_to_R_df(meta_data)
		exp_mat.to_csv('exp_mat.csv')
		meta_data.to_csv('meta_data.csv')

		subprocess.call(['R', '-f', './design_and_response_driver.R'])
		final_design = pandas.read_csv('design.tsv', sep='\t')
		final_response = pandas.read_csv('response.tsv', sep='\t')

		# restored the current directory
		os.chdir(cwd)
		return (final_design, final_response)

	def convert_to_R_df(self, df):
		new_df = pandas.DataFrame(df)
		import pdb; pdb.set_trace()
		for col in new_df:
			if new_df[col].dtype == 'bool':
				new_df[col] = [str(x).upper() for x in new_df[col]]