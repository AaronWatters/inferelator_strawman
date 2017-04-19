# Author: Nick De Veaux
# Short R file for communicating between python processes and legacy R file design_and_response.R

source('legacy/design_and_response.R')

meta.data <- read.table('meta_data.csv', sep = ',', header = 1, row.names = 1)
exp.mat <- read.table('exp_mat.csv', sep = ',', header = 1, row.names = 1)

source('params.cfg')

dr <- design.and.response(meta.data, exp.mat, delT.min, delT.max, tau)
dr$final_response_matrix
dr$final_design_matrix

write.table(as.matrix(dr$final_response_matrix), 'response.tsv', sep = '\t')
write.table(as.matrix(dr$final_design_matrix), 'design.tsv', sep = '\t')