"""

"""
from typing import Union

import us
import pandas as pd


def cast_fips_code(state_fips_code: Union[str, int]) -> str:
    """
    FIPS codes are technically two-digit strings representing a number between 0 and 99,
    e.g., "01" and "44". But it is very common that people pass them as integers.
    This guarantees they always appear as two-digit strings.

    Args:
        state_fips_code: A FIPS code as either a string or an int

    Return:
        The appropriately styled version of the code
    """
    if isinstance(state_fips_code, str):
        return state_fips_code
    if isinstance(state_fips_code, int):
        if state_fips_code <= 9:
            return '0' + str(state_fips_code)
        else:
            return str(state_fips_code)





def cast_zipcode(zipcode: Union[str, int]) -> str:
    """
    ZIP codes are five-digit strings, but it is very common that people pass them as
    integers. This guarantees that they always appear as five-digit strings

    Args:
        zipcode: A ZIP code

    Return:
        The appropriately styled version of the code
    """
    if isinstance(zipcode, int):
        return f"{zipcode:05d}"

    return zipcode


def puma_shapefile_name(state_fips_code: Union[str, int]) -> str:
    """
    Return the expected filename of the PUMA shapefile. Note that this assumes a 2019
    filename.

    Args:
        code: The FIPS code for the state of interest

    Return:
        The expected filename
    """
    return f"tl_2019_{state_fips_code}_puma10.zip"


def tract_shapefile_name(state_fips_code: Union[str, int]) -> str:
    """
    Return the expected filename of the tract shapefile. Note that this assumes a 2019
    filename.

    Args:
        code: The FIPS code for the state of interest

    Return:
        The expected filename
    """
    return f"tl_2019_{state_fips_code}_tract.zip"


def get_fips_code_from_abbr(state: str) -> str:
    """
    Given a state postal abbreviation, e.g., "RI", return its FIPS code, e.g., "44"

    Args:
        state: The abbreviation of the state

    Returns:
        The FIPS code of the state

    Raises:
    """
    obj = us.states.lookup(state)
    if not obj:
        raise KeyError(f"No such abbreviation: {state}")

    return obj.fips

def convert_to_df(data_dict: dict) -> pd.DataFrame:
    """
    Converts summary statistics returned by query_by_zip to a dataframe.

    Args:
        data_dict: the dictionary returned by query_by_zip

    Returns:
        pd.DataFrame containing the summary statistics by ZIP code

    Raises:
    """

    df = pd.DataFrame.from_dict(data_dict,orient='index')
    for col in df:
        df[col + "_mean"] = df[col].apply(lambda x: x["mean"])
        df[col + "_median"] = df[col].apply(lambda x: x["median"])
        df[col + "_std"] = df[col].apply(lambda x: x["std"])
        df.drop([col],axis=1, inplace=True)

    return df
