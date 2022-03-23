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
