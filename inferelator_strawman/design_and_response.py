import pandas
import subprocess
import os

class Legacy_Design_Response_Driver:

    legacy_directory = 'legacy'

    def get_design_response(self, exp_mat, meta_data, delT_min, delT_max, tau):
        # Change the current working directory
        cwd = os.getcwd()
        try:
            new_dir = os.path.dirname(os.path.abspath(__file__))
            os.chdir(new_dir)
            self.convert_to_R_df(meta_data)
            self.write_hyperparams(delT_min, delT_max, tau)
            exp_mat.to_csv('exp_mat.csv')
            meta_data.to_csv('meta_data.csv')
    
            subprocess.call(['R', '-f', './design_and_response_driver.R'])
            final_design = pandas.read_csv('design.tsv', sep='\t')
            final_response = pandas.read_csv('response.tsv', sep='\t')
        finally:
            # restore the current directory
            self.clean_up()
            os.chdir(cwd)

        return (final_design, final_response)

    def clean_up(self):
        os.remove('params.cfg')
        os.remove('meta_data.csv')
        os.remove('exp_mat.csv')
        os.remove('design.tsv')
        os.remove('response.tsv')

    def write_hyperparams(self, delT_min, delT_max, tau):
        with open('params.cfg', 'w') as configfile:
            configfile.write('delT.min <- {}\n'.format(delT_min))
            configfile.write('delT.max <- {}\n'.format(delT_max))
            configfile.write('tau <- {}'.format(tau))

    def convert_to_R_df(self, df):
        # This handles R <-> python incongruencies. 
        # For example True and False need to be converted to TRUE and FALSE
        new_df = pandas.DataFrame(df)
        for col in new_df:
            if new_df[col].dtype == 'bool':
                new_df[col] = [str(x).upper() for x in new_df[col]]

