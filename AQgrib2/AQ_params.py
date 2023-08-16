import pandas as pd
import numpy as np
import openpyxl

df=pd.read_excel('parameters_AQ_runs.xlsx')
df = df.apply(lambda x: x.str.replace('\n', '<br>') if x.dtype == 'object' else x)
md_table = df.to_markdown(index=False)
print(md_table)

