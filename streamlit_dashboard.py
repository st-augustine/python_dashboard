# %%
#IMPORT REQUIRED PACKAGES 

import pandas as pd
import numpy as np 
import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import panel as pn
pn.extension()
import plotly.graph_objects as go
import plotly.express as px

# %% [markdown]
# Boundaries
# --

# %%
#READ IN WARD BOUNDARIES 

wd22 = gpd.read_file("https://gist.github.com/joel-lbth/081ff5112ac66e6365a9846a6bc79409/raw/5371719f7fb24c286ce5839fc69e45c0c6049518/lbth-wards.topojson")

# %%
#PLOT WARD BOUNDARIES 

fig, ax =plt.subplots(1,1, figsize=(12, 12))
wd22.plot(facecolor='none', linewidth=1, edgecolor="black",ax=ax,legend=True).axis('off')

# %%
#READ IN LSOA BOUNDARIES 

lsoas = gpd.read_file('https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LSOA_2021_EW_BFC_V2/FeatureServer/0/query?where=LSOA21NM+like+%27Tower+Hamlets%25%27&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&relationParam=&returnGeodetic=false&outFields=LSOA21CD&returnGeometry=true&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=5&outSR=&defaultSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pgeojson&token=', driver="GeoJSON")

# %%
#READ IN OA BOUNDARIES 

oas= gpd.read_file('https://gist.githubusercontent.com/joel-lbth/8afdafefe431f6e1508cf59993a5b0d8/raw/bc7ce874ab02e6ae8b4b418cf16eff6386cf34c3/lbth_oa21_full.geojson', driver='GeoJSON')

# %% [markdown]
# Lookups
# --

# %%
#READ IN WARD LOOKUPS 

ward_lsoa_lookup= pd.read_csv('https://gist.githubusercontent.com/joel-lbth/da1b6f54f1cd076bf7336be7336de04b/raw/2e25cc5c14ae4a7914dcfc0c0a64dc131bab84bd/lbth_oa21_ward_lookup.csv')

# %% [markdown]
# Data
# --

# %%
#POPULATION DENSITY BY OA

popden_oa= pd.read_excel('https://ons-dp-prod-census-publication.s3.eu-west-2.amazonaws.com/TS006_population_density/atc-ts-demmig-ur-pd-oa-oa.xlsx',
    sheet_name='Table')


popden_oa.head()

# %%
#MERGE POPULATION DENSITY DATA WITH OA SPATIAL DATA

merged_oa_ward= oas.merge(popden_oa, left_on='OA21CD', right_on='Output Areas Code')

merged_oa_ward.head()

# %% [markdown]
# Mapping
# --

# %%
#MAKE PLOTY MAP OF POPULATION DENSITY BT OA

fig = px.choropleth(merged_oa_ward,
                   geojson=merged_oa_ward.geometry,
                   locations=merged_oa_ward.index,
                   color="Population Density",
                   projection="mercator")
fig.update_geos(fitbounds="locations", visible=False)
fig.show()

# %%
#st.plotly_chart(fig)

# %%
#MERGE WARD BOUNDARIES DF WITH LSOA DF

geo_df_merged= merged_oa_ward.merge(ward_lsoa_lookup, left_on='OA21CD', right_on='oa21cd')

geo_df_merged.head()

# %%
#AGGREGATE OAS INTO WARDS 

ward_oa_agg= geo_df_merged.dissolve(by='ward_name')

# %%
#PLOT AGGREGATED OA WARDS

wards, ax =plt.subplots(1,1, figsize=(12, 12))
ward_oa_agg.plot(facecolor='none', linewidth=1, edgecolor="black",ax=ax,legend=True).axis('off')

# %%
#MAKE PLOTY MAP OF POPULATION DENSITY BT WARD

fig = px.choropleth(ward_oa_agg,
                   geojson=ward_oa_agg.geometry,
                   locations=ward_oa_agg.index,
                   color="Population Density",
                   projection="mercator")
fig.update_geos(fitbounds="locations", visible=False)
fig.show()


