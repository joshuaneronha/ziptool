from pathlib import Path
from typing import Dict, List, Optional, Union

import numpy as np
import pandas as pd
import wquantiles

from .utils import cast_fips_code

FilenameType = Union[str, Path]


def get_acs_data(
    file: Union[FilenameType, pd.DataFrame],
    state_fips_code: Union[int, str],
    pumas: List[str],
    variables: Optional[Dict[str, str]] = None,
):
    """
    Pulls ACS data from a given file and extracts the data pertraining to a
    particular ZIP code. Can either return the full raw data or summary statistics.

    Args:
        file: a path to a datafile OR a dataframe containing ACS datafile
        variables: To extract summary statistics, pass a dictionary of the form::

                {
                    variable_of_interest_1: {
                        "null": null_val,
                        "type": type
                    },
                    variable_of_interest_2: {
                        "null": null_val,
                        "type": type
                    }...
                }

            variable_of_interest: the variable name you wish to summarize
            null_val: the value, as a float or integer, of null values to filter out.
            type: "household" or "individual", depending on the variable type

            To return the raw data, pass None.

        state_fips_code: an integer (or two-digit representation thereof)
            representing the state of interest's FIPS codes
        pumas: each PUMA of interest within the state and its ratio
            (returned by geo_conversion.tracts_to_puma)

    Returns:
        When variables of interest are passed, a dictionary of the form::

            {
                var_1: {
                    "mean": 46493.49,
                    "std": 57214.11,
                    "median": 29982.5
                }...
            }

        When variables of interest are NOT passed, a dictionary of the form::

            {puma_1: [puma1_df, ratio1], puma_2: [puma2_df, ratio2]...}
    """

    if isinstance(file, (str, Path)):
        data = pd.read_csv(file)
    elif isinstance(file, pd.DataFrame):
        data = file



    sub_state = data[data["STATEFIP"] == state_fips_code]

    # TODO(jn): Why is the cast to float necessary
    sub_state["HHWT"] = sub_state["HHWT"].astype(float)
    sub_state["PERWT"] = sub_state["PERWT"].astype(float)
    grouped = sub_state.groupby("PUMA")

    outer_dict = {}

    if variables is not None:

        for entry in variables:

            variable = entry
            null_val = variables[variable]["null"]
            var_type = variables[variable]["type"]

            avg_list = []
            median_list = []
            std_list = []
            removed_list = []

            for index, i in enumerate(pumas):
                this_puma = grouped.get_group(int(pumas.index[index]))

                rel_puma = (
                    this_puma
                    if var_type == "individual"
                    else this_puma[this_puma["PERNUM"] == 1]
                )
                chosen_weight = "PERWT" if var_type == "individual" else "HHWT"


                no_null = rel_puma[rel_puma[variable] != null_val]
                removed = (len(rel_puma) - len(no_null)) / len(rel_puma)
                removed_list.append(removed)

                no_null["weighted"] = no_null[variable] * no_null[chosen_weight]
                avg = no_null["weighted"].sum() / no_null[chosen_weight].sum()
                avg_list.append(avg * i)

                no_null['for_median_var'] = no_null[variable].astype('float64')

                median = wquantiles.median(no_null['for_median_var'], no_null[chosen_weight])

                median_list.append(median * i)

                std = np.sqrt(
                    (((no_null[variable] - avg) ** 2) * no_null[chosen_weight]).sum()
                    / (
                        (
                            (len(no_null[chosen_weight]) - 1)
                            / len(no_null[chosen_weight])
                        )
                        * no_null[chosen_weight].sum()
                    )
                )
                std_list.append(std * i)

            print(
                f"{np.mean(removed_list) * 100:0.2f}% of entries removed as null for variable {entry}"
            )

            outer_dict[variable] = {
                "mean": np.round(sum(avg_list),2),
                "std": np.round(sum(std_list),2),
                "median": np.round(sum(median_list),2)
            }
        return outer_dict

    else:
        # variables is None
        if len(pumas) == 1:
            this_puma = grouped.get_group(int(pumas.index[0]))
            return this_puma
        else:
            puma_dict = {}
            for index, i in enumerate(pumas):
                this_puma = grouped.get_group(int(pumas.index[index]))
                puma_dict[index] = [this_puma, i]
            return puma_dict
