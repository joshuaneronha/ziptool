import os
import tempfile
import urllib
from os.path import exists
import zipfile
import requests
import geopandas as gpd

shp_dir = tempfile.TemporaryDirectory()


def download_file(url: str, output_filename):
    """
    Download the URL to `output_filename`
    """

    os.chdir(shp_dir.name)

    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(output_filename, "wb") as outfile:
            for chunk in response.iter_content(chunk_size=8192):
                outfile.write(chunk)

download_file("https://www2.census.gov/geo/tiger/TIGER2019/PUMA/tl_2019_44_puma10.zip", "tl_2019_44_puma10.zip")

def get_state_intersections(state_fips_code: str) -> gpd.GeoDataFrame:

    os.chdir(shp_dir.name)

    ALBERS_EPSG_ID = 5760

    puma_name = "tl_2019_44_puma10.zip"
    tract_name = "tl_2019_44_puma10.zip"

    puma = gpd.read_file(puma_name).to_crs(
        epsg=ALBERS_EPSG_ID
    )
    tract = gpd.read_file(tract_name).to_crs(
        epsg=ALBERS_EPSG_ID
    )

    return gpd.overlay(puma, tract, how="intersection", keep_geom_type=False)


os.chdir(shp_dir.name)

get_state_intersections('44')

def download_data(state_fip_code):
    """
    For a given state (in particular its FIPS code), downloads its census tracts and PUMA shapefiles
    from the Census Bureau. The functions skips the download if the file already has been fetched!

    Args:
        state_fip_code: string representing the state of interest

    Returns:
        Saves .shp files for both PUMA and census tracts within the data directory.
    """

    os.chdir(shp_dir.name)

    tract_file = "tl_2019_" + state_fip_code + "_tract"
    puma_file = "tl_2019_" + state_fip_code + "_puma10"

    if exists(tract_file + ".shp"):
        pass
    else:
        req, _ = urllib.request.urlretrieve(
            "https://www2.census.gov/geo/tiger/TIGER2019/PUMA/" + puma_file + ".zip"
        )
        zipped = zipfile.ZipFile(req, "r")
        zipped.extractall()

        req, _ = urllib.request.urlretrieve(
            "https://www2.census.gov/geo/tiger/TIGER2019/TRACT/" + tract_file + ".zip"
        )
        zipped = zipfile.ZipFile(req, "r")
        zipped.extractall()

download_data('01')

shp_dir.cleanup()
