import tempfile
import json
import shutil
import urllib
from functools import lru_cache
import os
from os.path import exists
from pathlib import Path
from typing import Dict, List, Union
import pkg_resources
import tempfile

import geopandas as gpd
import numpy as np
import pandas as pd
import requests
import us
import wquantiles

pd.options.mode.chained_assignment = None

global shp_dir
shp_dir = tempfile.TemporaryDirectory()

from ziptool import geo_conversion, fetch_data, load, interface

def data_by_zip(zips: List[str], acs_data, variables):
    """
    This function takes in a list of ZIP codes and an ACS datafile and produces summary statistics
    for a given variable. It returns a dictionary containing the summary for each ZIP code.

    Args:
        zips: a list of zip codes, presented as strings (i.e. ['02835', '79901'])
        acs_data: either a pd.DataFrame of the ACS data OR a string of its filepath
        var_of_interest: the variable of interest as a string (i.e. 'HHINCOME')
        null_val: what defines a null entry. Often 9999999 or 0, check IPUMS documentation.
        type: whether the variable of interest is 'household' or 'individual' data
    """

    ans_dict = {}

    global hud_crosswalk

    # TODO(khw): zip is a keyword, change the name
    for zip in zips:
        tracts, state_fips_code = geo_conversion.zip_to_tract(zip)

        if sum([x[1] for x in tracts]) < 1e-7:
            raise ValueError(f"{zip} is not a valid residential zip code!")

        fetch_data.get_shape_files(state_fips_code)
        puma_ratios = geo_conversion.tracts_to_puma(tracts, state_fips_code)

        ans = interface.get_acs_data(acs_data, variables, int(state_fips_code), puma_ratios)
        ans_dict[zip] = ans

    return ans_dict
