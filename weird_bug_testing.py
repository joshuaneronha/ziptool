import numpy as np
import pandas as pd
from ziptool import geo_conversion, fetch_data

tracts, state_fips_code = geo_conversion.zip_to_tract('45103')
fetch_data.get_shape_files(state_fips_code, "2019")
puma_ratios = geo_conversion.tracts_to_puma(tracts, state_fips_code)

print(puma_ratios)
