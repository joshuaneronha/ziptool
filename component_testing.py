from ziptool.pipeline import *
import pandas as pd
import geopandas as gpd
import numpy as np
ipums_df = pd.read_csv('/Users/joshuaneronha/Documents/Brown/Policy Lab/ziptool/acs_data/usa_00013.csv')

tracts_to_puma_test(tracts, state_fips_code)

tracts, state_fips_code = zip_to_tract('02906')

    ALBERS_EPSG_ID = 5070

    intersection_gdf = get_state_intersections(state_fips_code)
    intersection_gdf["shape_area"] = intersection_gdf.area
    intersection_gdf["GEOID"] = intersection_gdf["GEOID"].astype("int")
    x = intersection_gdf[["GEOID", "PUMACE10", "shape_area"]].set_index("GEOID")
    x.head()


    y = intersection_gdf[["GEOID", "PUMACE10", "shape_area"]].groupby('GEOID').sum()
    y.head()



x.join(y,rsuffix='_total',how='inner')

    # TODO(jn): Make this comprehensible
    grouped_gdf = intersection_gdf.groupby("GEOID").agg(lambda x: list(x))[
        ["PUMACE10", "shape_area"]
    ]

grouped_gdf

    grouped_gdf["ratios"] = grouped_gdf["shape_area"].apply(
        lambda x: [y / sum(x) for y in x]
    )

    grouped_gdf

    sorted = grouped_gdf.loc[[int(x[0]) for x in tracts]][
        ["PUMACE10", "ratios"]
    ].explode(column=["PUMACE10", "ratios"])

sorted

    sorted["ratios"] = sorted["ratios"].apply(lambda x: 1 if x > 0.99 else x)
    out = sorted[sorted["ratios"] > (1 - 0.99)]
    joined = out.join(
        pd.DataFrame(tracts).astype({0: "int", 1: "float32"}).set_index(0)
    )
    joined["weighted_ratios"] = joined["ratios"] * joined[1]
    return joined.groupby("PUMACE10").sum()["weighted_ratios"]



tracts

get_shape_files('44')
