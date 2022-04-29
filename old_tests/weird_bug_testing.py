import numpy as np
import pandas as pd
from ziptool import geo_conversion, fetch_data

tracts, state_fips_code = geo_conversion.zip_to_tract('45103')
fetch_data.get_shape_files(state_fips_code, "2019")
puma_ratios = geo_conversion.tracts_to_puma(tracts, state_fips_code)

print(puma_ratios)

pd.Series([1,2,3,4,5]).shift(2)

data = pd.read_csv('tests/usa_00013.csv.zip')

substate = data[data['STATEFIP'] == 44]


def _group_weighted_median(df, group_col, val_col, weight_col):
    df = df[[group_col, val_col, weight_col]].dropna()
    df = df.sort_values(by=[group_col, val_col])

    cum_weight_high = df.groupby(group_col)[weight_col].cumsum() >= (0.5 * df.groupby(group_col)[weight_col].sum().repeat(df.groupby(group_col)[weight_col].count()).values)

    first_in_group = df[group_col] != df[group_col].shift(periods=1)


    return df[
        (first_in_group & cum_weight_high)
        | cum_weight_high & ~(cum_weight_high.shift(periods=1, fill_value=False))
    ].set_index(group_col)['HHINCOME']

x = _group_weighted_median(substate, 'PUMA', ['HHINCOME','EDUC', 'HHWT')
x
testing = pd.DataFrame()
pd.concat([testing,x,x],axis=1)
