import ziptool

sum_results = ziptool.data_by_zip(['79901'],'/Users/joshuaneronha/Documents/Brown/Policy Lab/ziptool/src/ziptool/resources/usa_00013.csv', {"HHINCOME": {"null": 9999999, "type": 'household'}})

sum_results

full_results = ziptool.data_by_zip(['79901'],'/Users/joshuaneronha/Documents/Brown/Policy Lab/ziptool/src/ziptool/resources/usa_00013.csv')

full_results['79901']

from ziptool.geo_conversion import zip_to_tract, tracts_to_puma
from ziptool.interface import get_acs_data

tracts, sfc = zip_to_tract('75204')

pumas = tracts_to_puma(tracts, sfc)

back = get_acs_data('/Users/joshuaneronha/Documents/Brown/Policy Lab/ziptool/src/ziptool/resources/usa_00013.csv', None, int(sfc), pumas)

back[1][1]
pumas
sum_results
sum_results.keys()
sum_results['79901']
full_results.keys()
full_results['77901']
sum_results.values()
full_results.values()
interface.get_acs_data()
from ziptool import geo_conversion

tracts, state = geo_conversion.zip_to_tract('79901')
tracts
state
pumas = geo_conversion.tracts_to_puma(tracts,'16')
pumas

ziptool.data_by_zip(['83701'],'/Users/joshuaneronha/Documents/Brown/Policy Lab/ziptool/src/ziptool/resources/usa_00013.csv', {"HHINCOME": {"null": 9999999, "type": 'household'}})

import pandas as pd
sample_data = pd.read_csv('/Users/joshuaneronha/Documents/Brown/Policy Lab/ziptool/src/ziptool/resources/usa_00013.csv')

onehh = sample_data[sample_data['PERNUM'] == 1]
onehh
nonull = onehh[onehh['HHINCOME'] != 9999999]
nonull['HHINCOME'].max()
nonull['weighted'] = nonull['HHINCOME'] * nonull['HHWT']
nonull['weighted'].sum() / nonull['HHWT'].sum()

import wquantiles

wquantiles.median(nonull['HHINCOME'], nonull['HHWT'])

summary_statistics = None
summary_statistics is None
