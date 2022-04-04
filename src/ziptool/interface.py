from pathlib import Path
from typing import Dict, List, Optional, Union

import numpy as np
import pandas as pd
import wquantiles

FilenameType = Union[str, Path]


def _group_weighted_mean(df, group_col, val_col, weight_col):
    df = df[[group_col, val_col, weight_col]].dropna()
    tmp_df = pd.DataFrame(
        {
            group_col: df[group_col],
            val_col: df[val_col] * df[weight_col],
        }
    )

    weighted_sums = tmp_df.groupby(group_col)[val_col].sum()
    total_weights = df.groupby(group_col)[weight_col].sum()
    return weighted_sums / total_weights


def _group_weighted_std(df, group_col, val_col, weight_col):
    df = df[[group_col, val_col, weight_col]].dropna()
    tmp_df = pd.DataFrame(
        {
            group_col: df[group_col],
            val_col: df[val_col] * df[weight_col],
            f"{val_col}2": (df[val_col] ** 2) * df[weight_col],
        }
    )

    weighted_sums = tmp_df.groupby(group_col)[val_col].sum()
    weighted_squares = tmp_df.groupby(group_col)[f"{val_col}2"].sum()
    total_weights = df.groupby(group_col)[weight_col].sum()
    num_in_group = df[group_col].size()

    return (
        (weighted_squares / total_weights - (weighted_sums / total_weights) ** 2)
        / (num_in_group - 1 + 1e-10)
        * num_in_group
    )


def _group_weighted_median(df, group_col, val_col, weight_col):
    df = df[[group_col, val_col, weight_col]].dropna()
    df = df.sort_values(by=["group_col", "val_col"])
    cum_weight_high = df.groupby(group_col)[weight_col].cumsum() >= 0.5
    first_in_group = df["group_col"] != df["group_col"].shift(periods=1)
    return df[
        (first_in_group & cum_weight_high)
        | cum_weight_high & ~(cum_weight_high.shift(periods=1, fill_value=False))
    ].set_index(group_col)


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
    else:
        raise TypeError(f"file must be a str, Path, or pd.DataFrame, not {type(file)}")

    sub_state = data[data["STATEFIP"] == state_fips_code].copy()

    dfs = []
    for key, value in variables.items():
        # Transform the null value to a pandas null value
        sub_state.loc[sub_state[key] == value["null"], key] = pd.NA

        # For household variables, put null values in extra rows
        if value["type"] != "individual":
            sub_state.loc[sub_state["PERNUM"] > 1, key] = pd.NA

        mean = _group_weighted_mean(
            sub_state, "PUMA", key, "PERWT" if value["type"] == "individual" else "HHWT"
        )
        std = _group_weighted_std(
            sub_state, "PUMA", key, "PERWT" if value["type"] == "individual" else "HHWT"
        )
        median = _group_weighted_median(
            sub_state, "PUMA", key, "PERWT" if value["type"] == "individual" else "HHWT"
        )
        dfs.append(
            pd.DataFrame(
                {f"{key}_mean": mean, f"{key}_std": std, f"{key}_median": median},
                index=mean.index,
            )
        )

    return pd.concat(dfs, axis=1)
