import pandas as pd

pd.options.mode.chained_assignment = None
import tempfile
from typing import List, Union

import geopandas as pd

from . import fetch_data, geo_conversion, interface


def data_by_zip(zips: List[str], acs_data, variables=None, year="2019"):
    """
    Extracts data from the ACS pertraining to a particular ZIP code.
    Can either return the full raw data or summary statistics.

    Args:
        zips: a list of zipcodes, represented as strings i.e. ['02906', '72901', ...]
        acs_data: a string representing the path of the datafile OR a dataframe containing ACS datafile
        variables (optional): To return the raw data, pass None. To extract summary statistics, pass a dictionary of the form: ::

                {
                    variable_of_interest_1: { #the variable name in IPUMS
                        "null": null_val, #the value (float or int) of null data
                        "type": type #"household" or "individual"
                    },
                    variable_of_interest_2: {
                        "null": null_val,
                        "type": type
                    }
                }
        year (optional): a string representing the year of shapefiles to use for matching PUMAs to ZIPs. Default is 2019.


    Returns:
        When variables of interest are passed, a dictionary of the form::

                {
                    zip_1: {
                        var_1: {
                            "mean": 12345.67,
                            "std": 23456.78,
                            "median": 34567.89
                        },
                        var_2: ...
                    },
                    zip_2: ...
                }

        When variables of interest are NOT passed, a dictionary of the form::

            {
                zip_1: [
                    [
                        puma_1_df,
                        puma_1_ratio
                    ],
                    [
                        puma_2_df,
                        puma_2_ratio
                    ],
                    ...,
                ],
                zip_2: ...
            }
    """

    ans_dict = {}

    global hud_crosswalk

    # TODO(khw): zip is a keyword, change the name
    for zip in zips:
        tracts, state_fips_code = geo_conversion.zip_to_tract(zip)

        if sum([x[1] for x in tracts]) < 1e-7:
            raise ValueError(f"{zip} is not a valid residential zip code!")

        fetch_data.get_shape_files(state_fips_code, year)
        puma_ratios = geo_conversion.tracts_to_puma(tracts, state_fips_code)

        ans = interface.get_acs_data(
            acs_data, int(state_fips_code), puma_ratios, variables
        )
        ans_dict[zip] = ans

    return ans_dict
