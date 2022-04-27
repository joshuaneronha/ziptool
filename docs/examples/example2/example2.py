import sys
from configuration import *
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import ipumspy
from ipumspy import IpumsApiClient, UsaExtract, readers, ddi

from ziptool.query_by_zip import data_by_zip

IPUMS_API_KEY = your_api_key
DOWNLOAD_DIR = Path(your_download_dir)

ipums = IpumsApiClient(IPUMS_API_KEY)

extract = UsaExtract(
    ["us2019a"],
    ["STATEFIP","PUMA","HHINCOME","ROOMS","BEDROOMS","CIHISPEED","FUELHEAT","VEHICLES","VALUEH"],
)

ipums.submit_extract(extract)
ipums.wait_for_extract(extract)
ipums.download_extract(extract, download_dir=DOWNLOAD_DIR)

ddi_file = list(DOWNLOAD_DIR.glob("*.xml"))[0]
ddi = ipumspy.readers.read_ipums_ddi(ddi_file)

ipums_df = ipumspy.readers.read_microdata(ddi,
            DOWNLOAD_DIR / ddi.file_description.filename)

HHINCOME_null = 9999999
BEDROOMS_null = 0
ROOMS_null = 0
CHISPEED_null = 0
FUELHEAT_null = 0
VEHICLES_null = 0
VALUEH_null = 9999999

def compare_variables(zips):

    fig, axes = plt.subplots(1,len(zips), figsize = (12,4))

    df = data_by_zip(zips, ipums_df)

    for index, (zip, value) in enumerate(df.items()):

        mask = [value["BEDROOMS"] > 0 ] and [value["ROOMS"] > 0 ] and \
        [value["CIHISPEED"] > 0 ] and [value["FUELHEAT"] > 0 ] and \
        [value["VEHICLES"] > 0 ] and [value["VALUEH"] != VALUEH_null] and \
        [value["HHINCOME"] != HHINCOME_null ]

        filtered = value[mask[0]]

        oneperson = filtered[filtered['PERNUM'] == 1]
        oneperson['CIHISPEED'] = oneperson['CIHISPEED'].replace(20,0)
        oneperson['CIHISPEED'] = oneperson['CIHISPEED'].replace([10,11,12,13,14,15,16,17],1)

        sns.heatmap(oneperson[["HHINCOME","ROOMS","BEDROOMS","CIHISPEED","VEHICLES","VALUEH"]].multiply(oneperson['HHWT'],axis = 'index').corr(), cmap = 'YlGnBu', vmin = 0, vmax = 1, ax = axes[index])
        axes[index].set_title(zip)

    plt.tight_layout()


compare_variables(['02835','10001','79901'])


compare_variables('10001',1)
compare_variables('79901',2)

plt.tight_layout()
