from os.path import exists, join
from pathlib import Path
from typing import Optional, Union

import requests

from ziptool.utils import cast_fips_code

from . import shp_dir

FilenameType = Union[str, Path]


def download_file(
    url: str, output_filename: FilenameType, session: Optional[requests.Session] = None
):
    """
    Downloads a file from the provided URL and saves it at the desired path.

    Args:
        url: a string representing the URL of the file you want to download
        output_filename: a FilenameType representing the desired download path

    Returns:
        None
    """

    session = session or requests

    with session.get(url, stream=True) as response:
        response.raise_for_status()
        with open(join(shp_dir.name, output_filename), "wb") as outfile:
            for chunk in response.iter_content(chunk_size=8192):
                outfile.write(chunk)


def get_shape_files(state_fips_code, year):
    """
    For a given state (in particular its FIPS code), downloads its census tracts and
    PUMA shapefiles from the Census Bureau. The functions skips the download if the
    file already has been fetched!

    Args:
        state_fips_code: string representing the state of interest
        year: string representing the year

    Returns:
        Saves .shp files for both PUMA and census tracts within the data directory.
    """
    state_fips_code = cast_fips_code(state_fips_code)

    tract_file = f"tl_{year}_{state_fips_code}_tract"
    puma_file = f"tl_{year}_{state_fips_code}_puma10"

    if exists(tract_file + ".zip"):
        return

    puma_url = f"https://www2.census.gov/geo/tiger/TIGER{year}/PUMA/{puma_file}.zip"
    download_file(puma_url, puma_url.split("/")[-1])

    tract_url = f"https://www2.census.gov/geo/tiger/TIGER{year}/TRACT/{tract_file}.zip"
    download_file(tract_url, tract_url.split("/")[-1])
