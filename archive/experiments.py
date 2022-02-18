import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

simple_data = pd.read_csv('usa_00007.csv')

simple_data.head()

only_ri = simple_data[simple_data['STATEFIP'] == 44]

ri_hier = only_ri.set_index(['CLUSTER','PERNUM'])

ri_hier.groupby('COUNTYFIP').sum()['PERWT']

top_ancs = ri_hier[['PERWT','ANCESTR1']].groupby('ANCESTR1').sum().sort_values('PERWT',ascending=False).reset_index()
top_ancs['ANCESTR1'] = top_ancs['ANCESTR1'].astype('int')
top_ancs = top_ancs.set_index('ANCESTR1')

top_ones = top_ancs.join(code)[1:20]
top_ones.set_axis(['PERWT', 'index', 'country'], axis=1, inplace=True)
top_ones.head()

plt.bar(top_ones['country'], top_ones['PERWT'])
yticks(top_ones['country'], rotation='vertical')

## this is the total number of households, pretty similar to Google (407,174)
ri_hier['HHWT'].groupby(level = 0).mean().sum()

## this is the total population -- since each row is one person! And confirmed by Google (1.059 million from 2019)
ri_hier['PERWT'].sum()

code = pd.read_table('usa_00006.cbk.txt',delimiter = '                ').reset_index()
code = code[code['ANC'].str.len() == 3]
code['ANC'] = code['ANC'].astype('int')
code = code.set_index('ANC')



fig = px.choropleth(top_ones, geojson=countries, locations='country', color='country',
                           color_continuous_scale="Viridis",
                           range_color=(0, 12)
                          )
