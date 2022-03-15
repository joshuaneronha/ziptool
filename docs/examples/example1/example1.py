from pathlib import Path
from config import your_api_key, your_download_dir
from ziptool.query_by_zip import data_by_zip

import ipumspy
from ipumspy import IpumsApiClient, UsaExtract, readers, ddi

IPUMS_API_KEY = your_api_key
DOWNLOAD_DIR = Path(your_download_dir)

ipums = IpumsApiClient(IPUMS_API_KEY)
#
# # extract = UsaExtract(
# #     ["us2019a"],
# #     ["STATEFIP","PUMA","HHINCOME","ANCESTR1"],
# # )
# # ipums.submit_extract(extract)
# # ipums.wait_for_extract(extract)
# # ipums.download_extract(extract, download_dir=DOWNLOAD_DIR)
#
ddi_file = list(DOWNLOAD_DIR.glob("*.xml"))[0]
ddi = ipumspy.readers.read_ipums_ddi(ddi_file)

ipums_df = ipumspy.readers.read_microdata(ddi, DOWNLOAD_DIR / ddi.file_description.filename)

# Jamestown, RI; 02835
# Kennebunkport, ME: 04046
# New Bedford, MA: 02740
# Stonington, CT: 06355
# Westerly, RI: 02804


# income_data = data_by_zip(['02835','04046','02740','06355','02804'], ipums_df,
#     {"HHINCOME": {"null": 9999999, "type":'household'}})

# out = data_by_zip(['02835','04046','02740','06355','02804'], ipums_df)

out = data_by_zip(['02835','04046','02740','06355','02804'], '/Users/joshuaneronha/Documents/Brown/Policy Lab/ziptool/src/ziptool/resources/usa_00013.csv')
# income_data = data_by_zip(['02835','04046','02740','06355','02804'], '/Users/joshuaneronha/Documents/Brown/Policy Lab/ziptool/src/ziptool/resources/usa_00013.csv',
#     {"HHINCOME": {"null": 9999999, "type":'household'}})
