import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

ALBERS_EPSG_ID = 2163

all_zips = gpd.read_file('zips_mapping/tl_2021_us_zcta520.shp').to_crs(epsg = ALBERS_EPSG_ID)
all_states = gpd.read_file('zips_mapping/tl_2021_us_state.shp').to_crs(epsg = ALBERS_EPSG_ID)
all_states = all_states[(all_states['STUSPS'] != 'AK') & (all_states['STUSPS'] != 'HI') & (all_states['STUSPS'] != 'VI') & (all_states['STUSPS'] != 'MP') & (all_states['STUSPS'] != 'GU') & (all_states['STUSPS'] != 'PR') & (all_states['STUSPS'] != 'AS')]

all_states.plot('GEOID',cmap='YlGnBu')
all_zips.plot()

intersection_gdf = gpd.overlay(all_zips, all_states, how = 'intersection')



mult_st_zips = intersection_gdf.groupby('ZCTA5CE20')['STUSPS'].count()[intersection_gdf.groupby('ZCTA5CE20')['STUSPS'].count() > 1].index.values

filtered_zips = intersection_gdf[intersection_gdf['ZCTA5CE20'].isin(mult_st_zips)][['ZCTA5CE20', 'STUSPS','geometry']]

filtered_zips['color'] = np.random.randint(1, 6, filtered_zips.shape[0])

fig, ax = plt.subplots(figsize = (32,16))
all_states.geometry.boundary.plot(color=None,edgecolor='k',linewidth = 0.35,ax=ax)
filtered_zips.geometry.boundary.plot(color=None,edgecolor='k',linewidth = 0.2,ax=ax)
filtered_zips.plot('color',ax=ax, cmap='YlGnBu')
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
plt.title('Multi-State ZIP Codes', fontdict = {'fontsize': 36})
