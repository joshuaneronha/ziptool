from config import your_api_key, your_download_dir
from ziptool.query_by_zip import data_by_zip
from ziptool.utils import convert_to_df
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path
import ipumspy
from ipumspy import IpumsApiClient, UsaExtract, readers, ddi

ylgnbu = ['#7fcdbb', '#41b6c4', '#225ea8', '#0c2c84', '#f29c33', '#666462']



IPUMS_API_KEY = your_api_key
DOWNLOAD_DIR = Path(your_download_dir)

# ipums = IpumsApiClient(IPUMS_API_KEY)
#
# extract = UsaExtract(
#     ["us2019a"],
#     ["STATEFIP","PUMA","HHINCOME","ANCESTR1"],
# )
# ipums.submit_extract(extract)
# ipums.wait_for_extract(extract)
# ipums.download_extract(extract, download_dir=DOWNLOAD_DIR)
#
ddi_file = list(DOWNLOAD_DIR.glob("*.xml"))[0]
ddi = ipumspy.readers.read_ipums_ddi(ddi_file)

ipums_df = ipumspy.readers.read_microdata(ddi, DOWNLOAD_DIR / ddi.file_description.filename)

# income_data = data_by_zip(['02835','04046','02740','06355','02804'], ipums_df,
#     {"HHINCOME": {"null": 9999999, "type":'household'}})
#
# income_df = convert_to_df(income_data)
# plt.bar(income_df.index, income_df['HHINCOME_mean'], color = ylgnbu[3])
# plt.title('Average Household Income')
# plt.show()


ancestry_info = ddi.get_variable_info('ANCESTR1')
ancestry_codes = ancestry_info.codes
top_codes = [ancestry_codes['Portuguese'], ancestry_codes['Irish, various subheads,'], ancestry_codes['Italian'], ancestry_codes['English']]



# Jamestown, RI; 02835
# Kennebunkport, ME: 04046
# New Bedford, MA: 02740
# Stonington, CT: 06355
# Westerly, RI: 02804


raw_dfs = data_by_zip(['02835','04046','02740','06355','02804'], ipums_df)

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
#
ax[1,2].axis('off')
fig.legend(['Portuguese','Irish','Italian','English','Other'], loc = 4)
plt.show()

# income_df = convert_to_df(income_data)
# plt.bar(income_df.index, income_df['HHINCOME_mean'], color = ylgnbu[3])
# plt.title('Average Household Income')
# plt.show()



# plt.bar

# out = data_by_zip(['02835','04046','02740','06355','02804'], '/Users/joshuaneronha/Documents/Brown/Policy Lab/ziptool/src/ziptool/resources/usa_00013.csv')
