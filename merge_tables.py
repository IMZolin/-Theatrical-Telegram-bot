import os
import pandas as pd
#import xlsxwriter
table1 = pd.read_excel('all_performance_dict.xlsx')
table2 = pd.read_excel('table.xlsx')
table3 = pd.read_excel('data.xlsx')
total = pd.concat([table1, table2, table3])
total.to_excel('theatres_table.xlsx', index=False)