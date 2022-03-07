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

def download_file(url: str, output_filename: FilenameType):
    """
    Downloads a file from the provided URL and saves it at the desired path.

    Args:
        url: a string representing the URL of the file you want to download
        output_filename: a FilenameType representing the desired download path

    Returns:
        None
    """

    os.chdir(shp_dir.name)

    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(output_filename, "wb") as outfile:
            for chunk in response.iter_content(chunk_size=8192):
                outfile.write(chunk)

def get_shape_files(state_fips_code):
    """

    For a given state (in particular its FIPS code), downloads its census tracts and PUMA shapefiles
    from the Census Bureau. The functions skips the download if the file already has been fetched!

    Args:
        state_fips_code: string representing the state of interest

    Returns:
        Saves .shp files for both PUMA and census tracts within the data directory.
    """


    tract_file = "tl_2019_" + state_fips_code + "_tract"
    puma_file = "tl_2019_" + state_fips_code + "_puma10"

    if exists(tract_file + ".zip"):
        pass
    else:
        puma_url = "https://www2.census.gov/geo/tiger/TIGER2019/PUMA/" + puma_file + ".zip"
        download_file(puma_url, puma_url.split('/')[-1])

        tract_url = "https://www2.census.gov/geo/tiger/TIGER2019/TRACT/" + tract_file + ".zip"
        download_file(tract_url, tract_url.split('/')[-1])
