import pandas as pd

pd.options.mode.chained_assignment = None
import geopandas as pd
import tempfile
from typing import List, Union


from . import fetch_data, geo_conversion, interface


def data_by_zip(zips: List[str], acs_data, variables=None):
    """
    Extracts data from the ACS pertraining to a particular ZIP code.
    Can either return the full raw data or summary statistics.

    Args:
        zips: a list of zipcodes, represented as strings i.e. ['02906', '72901', ...]
        acs_data: a string representing the path of the datafile OR a dataframe containing ACS datafile
        variables:
            *To extract summary statistics, pass a dictionary of the form:*::

                {
                    variable_of_interest_1: {
                        "null": null_val,
                        "type": type
                    },
                    variable_of_interest_2: {
                        "null": null_val,
                        "type": type
                    }
                }

            variable_of_interest: the variable name you wish to summarize
            null_val: the value, as a float or integer, of null values to filter out.
            type: "household" or "individual", depending on the variable type

            *To return the raw data:*
                Pass None

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

        fetch_data.get_shape_files(state_fips_code)
        puma_ratios = geo_conversion.tracts_to_puma(tracts, state_fips_code)

        ans = interface.get_acs_data(
            acs_data, int(state_fips_code), puma_ratios, variables
        )
        ans_dict[zip] = ans

    return ans_dict
