import pandas as pd
import geopandas as gpd
import numpy as np

ALBERS_EPSG_ID = 5070

ri_puma = gpd.read_file('data/tl_2019_44_puma10.shp').to_crs(epsg = ALBERS_EPSG_ID)

ri_puma.plot()

ri_tract = gpd.read_file('data/tl_2019_44_tract.shp').to_crs(epsg = ALBERS_EPSG_ID)

ri_tract.plot()

intersection_gdf = gpd.overlay(ri_puma, ri_tract, how = 'intersection')

intersection_gdf["shape_area"] = intersection_gdf.area

grouped_gdf = intersection_gdf.groupby("GEOID").agg(lambda x: list(x))[['PUMACE10', 'shape_area']]

grouped_gdf['ratios'] = grouped_gdf['shape_area'].apply(lambda x: [y / sum(x) for y in x])


grouped_gdf[['PUMACE10','ratios']].head(50)


grouped_gdf.loc['44005041300']

zips = pd.read_excel('ZIP_TRACT_122021.xlsx')
zips[(zips['usps_zip_pref_state'] == 'RI') & (zips['zip'] == 2912)]



tract_area_s = intersection_gdf.groupby("TRACTCE")["shape_area"].agg({
	"max_area": "max",
	"total_area": "sum"
})
tract_area_s["pct_max_area"] = tract_area_s["max_area"] / tract_area_s["total_area"]


# ALBERS_EPSG_ID = 102003
#
# puma_gdf = gpd.read_file(path / to / puma)
# tract_gdf = gpd.read_file(path / to / tract)
#
# puma_gdf = puma_gdf.to_crs(epsg=ALBERS_EPSG_ID)
# tract_gdf = tract_gdf.to_crs(epsg=ALBERS_EPSG_ID)
#
# intersection_gdf = gpd.overlay(puma_gdf, tract_gdf, how="intersection")
#
# intersection_gdf["shape_area"] = intersection_gdf.area
# tract_area_s = intersection_gdf.groupby("tract_id")["shape_area"].agg({
# 	"max_area": "max",
# 	"total_area": "sum",
# })
# tract_area_s["pct_max_area"] = tract_area_s["max_area"] / tract_area_s["total_area"]
#
# tract_area_s["pct_max_area"].hist(bins=np.arange(0, 1.01, 0.05))
