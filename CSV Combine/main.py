from codecs import ignore_errors
import csv
from pprint import pprint as pp
import pandas as pd
import os

os.chdir('Classic-Imports-and-Design\CSV Combine\csvs')
cwd = os.path.abspath('')
files = os.listdir(cwd)

df = pd.DataFrame()
for file in files:
    if file.endswith('.xlsx'):
        df = df.append(pd.read_excel(file, header=None, skiprows=[0]), ignore_index=True)
df.head()
df.to_excel('output.xlsx')

