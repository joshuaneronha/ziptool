from configuration import *
import pandas as pd
import numpy as np
from pathlib import Path

import ipumspy
from ipumspy import IpumsApiClient, UsaExtract, readers, ddi

IPUMS_API_KEY = your_api_key
DOWNLOAD_DIR = Path(your_download_dir)

ipums = IpumsApiClient(IPUMS_API_KEY)

extract = UsaExtract(
    ["us2019a"],
    ["STATEFIP","PUMA","HHINCOME","ANCESTR1"],
)
# ipums.submit_extract(extract)
# ipums.wait_for_extract(extract)
# ipums.download_extract(extract, download_dir=DOWNLOAD_DIR)

ddi_file = list(DOWNLOAD_DIR.glob("*.xml"))[0]
ddi = ipumspy.readers.read_ipums_ddi(ddi_file)

ipums_df = ipumspy.readers.read_microdata(ddi,
            DOWNLOAD_DIR / ddi.file_description.filename)

from ziptool.query_by_zip import data_by_zip

income_df = data_by_zip(['02740','02804','02835','04046','06355'], ipums_df,
    {"HHINCOME": {"null": 9999999, "type":'household'}})
# income_df = convert_to_df(income_data)

import matplotlib.pyplot as plt
ylgnbu = ['#7fcdbb', '#41b6c4', '#225ea8',
          '#0c2c84', '#f29c33', '#666462']
#defining our colorscale

plt.bar(income_df.index, income_df['HHINCOME_mean'], color = ylgnbu[3])
plt.title('Average Household Income')
plt.show()

raw_dfs = data_by_zip(['02835','04046','02740','06355','02804'], ipums_df)

ancestry_info = ddi.get_variable_info('ANCESTR1')
ancestry_codes = ancestry_info.codes
top_codes = [ancestry_codes['Portuguese'],
             ancestry_codes['Irish, various subheads,'],
             ancestry_codes['Italian'],
             ancestry_codes['English']]

fig, ax = plt.subplots(2,3)

for i,zip in enumerate(['02835','04046','02740','06355','02804']):
    row = int(np.floor(i/3))
    column = int(i % 3)
    data = raw_dfs[zip]
    ancestry_data= data.groupby('ANCESTR1').sum()['PERWT']
    other = pd.Series([ancestry_data.loc[~ancestry_data.index.isin(top_codes + [ancestry_codes['Not Reported']])].sum()],index=[0])
    to_plot = ancestry_data[top_codes].append(other)
    ax[row,column].pie(to_plot, colors = ylgnbu)
    ax[row,column].set_title(zip)

ax[1,2].axis('off')
fig.legend(['Portuguese','Irish','Italian','English','Other'], loc = 4)
plt.show()
