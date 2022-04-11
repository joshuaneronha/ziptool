import ipumspy
from ipumspy import IpumsApiClient, UsaExtract, ddi, readers
import numpy as np
import pandas as pd
from ziptool import geo_conversion, fetch_data

# tracts, state_fips_code = geo_conversion.zip_to_tract('02835')
# fetch_data.get_shape_files(state_fips_code, "2019")
# puma_ratios = geo_conversion.tracts_to_puma(tracts, state_fips_code)

from ziptool.query_by_zip import data_by_zip

test_results = data_by_zip(
    ["02835", "45103"],
    'tests/usa_00013.csv.zip',
    {
        "HHINCOME": {"null": 9999999, "type": "household"},
        "EDUC": {"null": 0, "type": "individual"},
    },
)

test_results.round(2).to_dict(orient = 'index')

print(test_results.round(2).to_dict(orient = 'index'))

# out = get_acs_data('tests/usa_00013.csv.zip', state_fips_code, puma_ratios,
# {"HHINCOME": {"null": 9999999, "type": "household"},
#             "EDUC": {"null": 0, "type": "individual"},
#         })
#
# print(out)
