# import json
# import shutil
# import urllib
# from functools import lru_cache
# import os
# from os.path import exists
# from pathlib import Path
# from typing import Dict, List, Union
# import pkg_resources
# import tempfile
#
# import geopandas as gpd
# import numpy as np
# import pandas as pd
# import requests
# import us
# import wquantiles
# from ziptool import shp_dir

# global shp_dir
# shp_dir = tempfile.TemporaryDirectory()

# pd.options.mode.chained_assignment = None  # default='warn'

# FilenameType = Union[str, Path]

# def load_crosswalk():
#     stream = pkg_resources.resource_stream(__name__, 'resources/ZIP_TRACT_122021.XLSX')
#     return pd.read_excel(stream)
#
# def load_test_data():
#     stream = pkg_resources.resource_stream(__name__, 'resources/usa_00013.csv')
#     return pd.read_csv(stream)

# @lru_cache(maxsize=100)
# def get_state_intersections(state_fips_code: str) -> gpd.GeoDataFrame:
#
#     os.chdir(shp_dir.name)
#
#     puma_name = 'tl_2019_' + state_fips_code + "_puma10.zip"
#     tract_name = 'tl_2019_' + state_fips_code + "_tract.zip"
#
#     puma = gpd.read_file(puma_name).to_crs(
#         epsg=ALBERS_EPSG_ID
#     )
#     tract = gpd.read_file(tract_name).to_crs(
#         epsg=ALBERS_EPSG_ID
#     )
#
#     return gpd.overlay(puma, tract, how="intersection", keep_geom_type=False)

# def download_file(url: str, output_filename: FilenameType):
#     """
#     Download the URL to `output_filename`
#     """
#
#     os.chdir(shp_dir.name)
#
#     with requests.get(url, stream=True) as response:
#         response.raise_for_status()
#         with open(output_filename, "wb") as outfile:
#             for chunk in response.iter_content(chunk_size=8192):
#                 outfile.write(chunk)

# def get_fips_code_from_abbr(state: str) -> str:
#     """
#     Given a state postal abbreviation, e.g., "RI", return its FIPS code, e.g., "44"
#
#     Args:
#         state: The abbreviation of the state
#
#     Returns:
#         The FIPS code of the state
#
#     Raises:
#     """
#     obj = us.states.lookup(state)
#     if not obj:
#         raise KeyError(f"No such abbreviation: {state}")
#
#     return obj.fips

# var_of_interest, null_val, type
# def data_by_zip(zips: List[str], acs_data, variables):
#     """
#     This function takes in a list of ZIP codes and an ACS datafile and produces summary statistics
#     for a given variable. It returns a dictionary containing the summary for each ZIP code.
#
#     Args:
#         zips: a list of zip codes, presented as strings (i.e. ['02835', '79901'])
#         acs_data: either a pd.DataFrame of the ACS data OR a string of its filepath
#         var_of_interest: the variable of interest as a string (i.e. 'HHINCOME')
#         null_val: what defines a null entry. Often 9999999 or 0, check IPUMS documentation.
#         type: whether the variable of interest is 'household' or 'individual' data
#     """
#
#     ans_dict = {}
#
#     global hud_crosswalk
#
#     # TODO(khw): zip is a keyword, change the name
#     for zip in zips:
#         tracts, state_fips_code = zip_to_tract(zip)
#
#         if sum([x[1] for x in tracts]) < 1e-7:
#             raise ValueError(f"{zip} is not a valid residential zip code!")
#
#         get_shape_files(state_fips_code)
#         puma_ratios = tracts_to_puma(tracts, state_fips_code)
#
#         ans = get_acs_data(acs_data, variables, int(state_fips_code), puma_ratios)
#         ans_dict[zip] = ans
#
#     return ans_dict


# def get_shape_files(state_fips_code):
#     """
#
#     For a given state (in particular its FIPS code), downloads its census tracts and PUMA shapefiles
#     from the Census Bureau. The functions skips the download if the file already has been fetched!
#
#     Args:
#         state_fips_code: string representing the state of interest
#
#     Returns:
#         Saves .shp files for both PUMA and census tracts within the data directory.
#     """
#
#
#     tract_file = "tl_2019_" + state_fips_code + "_tract"
#     puma_file = "tl_2019_" + state_fips_code + "_puma10"
#
#     if exists(tract_file + ".zip"):
#         pass
#     else:
#         puma_url = "https://www2.census.gov/geo/tiger/TIGER2019/PUMA/" + puma_file + ".zip"
#         download_file(puma_url, puma_url.split('/')[-1])
#
#         tract_url = "https://www2.census.gov/geo/tiger/TIGER2019/TRACT/" + tract_file + ".zip"
#         download_file(tract_url, tract_url.split('/')[-1])

# def zip_to_tract(zip):
#     """
#     For a given ZIP code, uses HUD Crosswalk data (https://www.huduser.gov/portal/datasets/usps_crosswalk.html)
#     to find the ratio of persons in each census tract for the given ZIP code.
#
#     Args:
#         zip: the five-digit ZIP code of interest, written as a string
#
#     Returns:
#         List containing the same number of entries as census tracts within the ZIP code. Each entry is a list,
#         entry 0 is the census tact and entry 1 is the residential ratio of the census tract within that ZIP.
#     """
#
#     hud_crosswalk = load_crosswalk()
#
#     try:
#         zip_str = zip
#         zip = int(zip)
#     except ValueError:
#         pass
#
#     contained = hud_crosswalk[hud_crosswalk["zip"] == zip][["tract", "res_ratio"]]
#     try:
#         state = hud_crosswalk[hud_crosswalk["zip"] == zip]["usps_zip_pref_state"].iloc[
#             0
#         ]
#     except IndexError:
#         raise KeyError(zip_str + " is not a valid ZIP code!")
#     return contained.values.tolist(), get_fips_code_from_abbr(state)
#
#
# def tracts_to_puma(tracts, state_fips_code: str):
#     """
#     Takes in a list of tracts and ratios for a given zip code (in a given state) and returns the PUMAs
#     composing the ZIP code with ratios (i.e. 88% in PUMA 00101 and 12% in PUMA 00102).
#
#     Args:
#         tracts: a 2D list generated by zip_to_tract containing census tracts and weighted_ratios
#         state_fips_code: string representing state of interest
#
#     Returns:
#         series containing ratio of population for each PUMA
#     """
#     global ALBERS_EPSG_ID
#     ALBERS_EPSG_ID = 5070
#
#     intersection_gdf = get_state_intersections(state_fips_code)
#     intersection_gdf["shape_area"] = intersection_gdf.area
#     intersection_gdf["GEOID"] = intersection_gdf["GEOID"].astype("int")
#
#     intersection_gdf = intersection_gdf[["GEOID", "PUMACE10", "shape_area"]]
#     tract_areas = intersection_gdf[["GEOID", "PUMACE10", "shape_area"]].groupby('GEOID').sum()
#
#     intersection_gdf = intersection_gdf.set_index("GEOID")
#
#     joined = intersection_gdf.join(tract_areas,rsuffix='_total',how='inner')
#     joined['ratio'] = joined['shape_area'] / joined['shape_area_total']
#
#     tracts_of_interest = [int(x[0]) for x in tracts]
#
#     sorted = joined[["PUMACE10", "ratio"]].loc[tracts_of_interest]
#     sorted["rounded_ratio"] = sorted["ratio"].apply(lambda x: 1 if x > 0.99 else x)
#     rounded = sorted[sorted["rounded_ratio"] > (1 - 0.99)]
#     summary =  rounded.join(
#             pd.DataFrame(tracts, columns = ["GEOID", "PUMARAT"]).astype({"GEOID": "int", "PUMARAT": "float32"}).set_index("GEOID")
#         )
#     summary["weighted_ratios"] = summary["rounded_ratio"] * summary["PUMARAT"]
#
#     return summary.groupby("PUMACE10").sum()["weighted_ratios"]

# def get_acs_data(
#     file: Union[FilenameType, pd.DataFrame],
#     variables: Dict[str, str],
#     state_fips_code,
#     pumas,
# ):
#     if isinstance(file, (str, Path)):
#         data = pd.read_csv(file)
#     elif isinstance(file, pd.DataFrame):
#         data = file
#
#     sub_state = data[data["STATEFIP"] == state_fips_code]
#     # TODO(jn): Why is the cast to float necessary
#     sub_state["HHWT"] = sub_state["HHWT"].astype(float)
#     sub_state["PERWT"] = sub_state["PERWT"].astype(float)
#     grouped = sub_state.groupby("PUMA")
#
#     outer_dict = {}
#
#     for entry in variables:
#
#         variable = entry
#         null_val = variables[variable]["null"]
#         var_type = variables[variable]["type"]
#
#         avg_list = []
#         median_list = []
#         std_list = []
#
#         # TODO(jn) something like this to DRY this out
#
#         for index, i in enumerate(pumas):
#             this_puma = grouped.get_group(int(pumas.index[index]))
#
#             rel_puma = this_puma if var_type == "individual" else this_puma[this_puma["PERNUM"] == 1]
#             chosen_weight = "PERWT" if var_type == "individual" else "HHWT"
#             print(chosen_weight)
#
#             # rel_puma[variable] = rel_puma[variable].astype(float)
#             no_null = rel_puma[rel_puma[variable] != null_val]
#
#             no_null["weighted"] = no_null[variable] * no_null[chosen_weight]
#             avg = no_null["weighted"].sum() / no_null[chosen_weight].sum()
#             avg_list.append(avg * i)
#
#             median = wquantiles.median(no_null[variable], no_null[chosen_weight])
#             median_list.append(median * i)
#
#             std = np.sqrt(
#                     (((no_null[variable] - avg) ** 2) * no_null[chosen_weight]).sum()
#                     / (
#                         ((len(no_null[chosen_weight]) - 1) / len(no_null[chosen_weight]))
#                         * no_null[chosen_weight].sum()
#                     )
#                 )
#             std_list.append(std * i)
#
#         outer_dict[variable] = {
#             "mean": round(sum(avg_list), 2),
#             "std": round(sum(std_list), 2),
#             "median": round(sum(median_list), 2),
#         }
#
#     return outer_dict

# ipums_df = pd.read_csv('acs_data/usa_00013.csv')
# # pulled = data_by_zip(['02835', '79901','75204', '90210'],ipums_df, {"HHINCOME": {"null": 9999999, "type": 'household'}})
# # print(pulled)
# pulled = data_by_zip(['96804'],ipums_df, {"HHINCOME": {"null": 9999999, "type": 'household'}})
# print(pulled)
