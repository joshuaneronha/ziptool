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

from ziptool import shp_dir

FilenameType = Union[str, Path]

def get_acs_data(
    file: Union[FilenameType, pd.DataFrame],
    variables: Dict[str, str],
    state_fips_code,
    pumas,
):
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

    for entry in variables:

        variable = entry
        null_val = variables[variable]["null"]
        var_type = variables[variable]["type"]

        avg_list = []
        median_list = []
        std_list = []

        # TODO(jn) something like this to DRY this out

        for index, i in enumerate(pumas):
            this_puma = grouped.get_group(int(pumas.index[index]))

            rel_puma = this_puma if var_type == "individual" else this_puma[this_puma["PERNUM"] == 1]
            chosen_weight = "PERWT" if var_type == "individual" else "HHWT"

            # rel_puma[variable] = rel_puma[variable].astype(float)
            no_null = rel_puma[rel_puma[variable] != null_val]

            no_null["weighted"] = no_null[variable] * no_null[chosen_weight]
            avg = no_null["weighted"].sum() / no_null[chosen_weight].sum()
            avg_list.append(avg * i)

            median = wquantiles.median(no_null[variable], no_null[chosen_weight])
            median_list.append(median * i)

            std = np.sqrt(
                    (((no_null[variable] - avg) ** 2) * no_null[chosen_weight]).sum()
                    / (
                        ((len(no_null[chosen_weight]) - 1) / len(no_null[chosen_weight]))
                        * no_null[chosen_weight].sum()
                    )
                )
            std_list.append(std * i)

        outer_dict[variable] = {
            "mean": round(sum(avg_list), 2),
            "std": round(sum(std_list), 2),
            "median": round(sum(median_list), 2),
        }

    return outer_dict
