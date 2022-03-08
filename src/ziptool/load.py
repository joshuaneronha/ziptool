import pandas as pd
import pkg_resources


def load_crosswalk():
    """
    Loads in HUDS crosswalk file that is stored as a project resource.

    Args:
        None

    Returns:
        A dataframe reprenting HUD crosswalk data.
    """
    stream = pkg_resources.resource_stream(
        __name__, "resources/zip_tract_122021.parquet"
    )
    return pd.read_parquet(stream)


def load_test_data():
    """
    Loads in test data that is used to verify the data processing pipeline's integrity.

    Args:
        None

    Returns:
        A dataframe reprenting the sample data.
    """
    stream = pkg_resources.resource_stream(__name__, "resources/usa_00013.csv")
    return pd.read_csv(stream)
