# %%
#IMPORT REQUIRED PACKAGES 

import pandas as pd
import numpy as np 
import streamlit as st
import geopandas as gpd
import plotly.express as px
import matplotlib as plt

# %% [markdown]
# Boundaries
# --

# %%
# 2022 ward boundaries
try:
  wd22 = gpd.read_file('lbth_wd22.geojson')
except Exception:
  wd22 = gpd.read_file('https://gist.github.com/joel-lbth/081ff5112ac66e6365a9846a6bc79409/raw/5371719f7fb24c286ce5839fc69e45c0c6049518/lbth-wards.topojson')
  wd22.to_file('wd22.geojson', driver='GeoJSON')

# %%
#PLOT WARD BOUNDARIES 

fig, ax =plt.subplots(1,1, figsize=(12, 12))
wd22.plot(facecolor='none', linewidth=1, edgecolor="black",ax=ax,legend=True).axis('off')

# %%
# 2021 lsoa boundaries
try:
  lsoa21 = gpd.read_file('lbth_lsoa21.geojson')
except Exception:
  lsoa21 = gpd.read_file('https://gist.github.com/joel-lbth/5c1a6de137eb092bff61e82bd37996aa/raw/e8efb126c04045c6730d6bbbae3863dd5e80dd80/lbth-lsoa21.geojson')
  lsoa21.to_file('lbth_lsoa21.geojson', driver='GeoJSON')

# %%
# 2021 oa boundaries
try:
  oa21 = gpd.read_file('lbth_oa21.geojson')
except Exception:
  oa21 = gpd.read_file('https://gist.githubusercontent.com/joel-lbth/9cd8cbf8078d78954bb011a0927001a3/raw/cc247b708b2e52c549c03af5923b9dc8d3eec5af/lbth_oa21.geojson')
  oa21.to_file('lbth_oa21.geojson', driver='GeoJSON')

# %% [markdown]
# Lookups
# --

# %%
# ward oa lookup
try:
  wd_oa_lkup = pd.read_csv('wd_lsoa_lkup21.csv')
except Exception:
  wd_oa_lkup = pd.read_csv('https://gist.githubusercontent.com/joel-lbth/da1b6f54f1cd076bf7336be7336de04b/raw/2e25cc5c14ae4a7914dcfc0c0a64dc131bab84bd/lbth_oa21_ward_lookup.csv')
  wd_oa_lkup.to_csv('lbth_wd_oa_lkup.csv')

# %% [markdown]
# Functions
# ==

# %%
def merge_spatial_data(gdf, df, left_on="", right_on=""):
    gdf=gdf.merge(df, left_on=left_on, right_on=right_on)
    return gdf

# %% [markdown]
# Mapping
# --

# %%
#POPULATION DENSITY BY OA

try:
  popden_oa = pd.read_csv('lbth_census_2021_popden_oa.csv')
except:
  popden_oa = pd.read_csv('https://www.nomisweb.co.uk/api/v01/dataset/NM_2026_1.data.csv?date=latest&geography=629165479...629165982,629303674...629303812,629317322...629317326,629317336...629317343,629317349...629317360,629317362...629317366,629317371,629317374,629317376,629317378,629317379,629317381,629317385,629317388...629317392,629317394...629317397,629317399...629317403,629317405...629317407,629317409,629317411,629317412,629317416...629317420,629317422...629317424,629317426,629317429...629317434,629317436,629317437,629317440...629317442,629317444...629317450,629317452...629317456,629317459...629317461,629317463,629317466...629317468,629317472,629317474...629317479,629317481,629317483,629317486,629317487,629317490,629317492,629317494,629317495,629317497,629317499...629317502,629317504,629317505,629317507...629317509,629317512...629317514,629317517,629317520,629317523,629317525,629317527,629317531,629317534,629317535,629317537,629317538,629317540,629317543...629317548,629317551,629317554,629317555,629317558,629317560,629317562,629317563,629317565,629317566,629317569...629317573,629317576...629317578,629317580,629317582,629317584,629317585,629317587,629317590...629317592,629317594,629317596...629317599,629317601,629317603,629317604,629317606,629317607,629317610,629317612,629317613,629317615...629317617,629317619...629317621,629317623,629317625...629317629,629317631...629317634,629317636,629317640,629317648,629317650...629317659,629317662,629317663,629317666...629317669,629317672...629317687,629317689,629317691,629317694,629317695,629317697,629317698,629317700,629317701,629317703,629317704,629317706,629317707,629317711...629317714,629317716,629317718...629317720,629317722...629317724,629317726,629317729,629317731,629317733,629317736...629317742,629317744,629317746...629317748,629323624,629323625&cell=0&measures=20100&select=date_name,geography_name,geography_code,cell_name,measures_name,obs_value,obs_status_name')
  popden_oa.to_csv('lbth_census_2021_popden_oa.csv')

# %%
popden_merge=merge_spatial_data(oa21, popden_oa,"OA21CD", "GEOGRAPHY_CODE")

# %%
popden_oa.describe()  #highly skewed df


# %%
# return a dataframe without inter quartile range outliers on a given dataframe column
def iqr_df(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    trueList = ~((df[column] < (Q1 - 3 * IQR)) | (df[column] > (Q3 + 3 * IQR)))
    return df[trueList]

# %%
#plot population density by oa

popden_merge_iq=iqr_df(popden_merge,'OBS_VALUE')

#fig = px.choropleth(data_frame=popden_merge_iq,
                   #geojson=popden_merge_iq.geometry,
                   #locations=popden_merge_iq.index,
                   #color="OBS_VALUE",
                   #range_color=(0, 100000),
                   #color_continuous_scale = 'viridis_r',
                   #projection='mercator')
##fig.update_geos(fitbounds="geojson", visible=False)
#fig.show()

# %%
#MERGE WARD BOUNDARIES DF WITH LSOA DF

popden_wd_oa_merged= popden_merge.merge(wd_oa_lkup, left_on='OA21CD', right_on='oa21cd')

popden_wd_oa_merged.head()

# %%
#PLOT AGGREGATED OA WARDS

wards, ax =plt.subplots(1,1, figsize=(12, 12))
popden_wd_oa_merged.dissolve(by='ward_name').plot(facecolor='none', linewidth=1, edgecolor="black",ax=ax,legend=True).axis('off')

# %%
#MAKE PLOTY MAP OF POPULATION DENSITY BT WARD

#fig = px.choropleth(popden_wd_oa_merged.dissolve(by='ward_name'),
                   #geojson=popden_wd_oa_merged.dissolve(by='ward_name').geometry,
                   #locations=popden_wd_oa_merged.dissolve(by='ward_name').index,
                   #color="OBS_VALUE",
                   #color_continuous_scale = 'viridis_r',
                   #projection="mercator",
                   #hover_name=popden_wd_oa_merged.dissolve(by='ward_name').index,
                   #hover_data=['OBS_VALUE'])
#fig.update_geos(fitbounds="locations", visible=False)
#fig.show()

# %%
#READ IN DEPRIVATION DATASET 

try:
  deprivation_oa = pd.read_csv('lbth_census_2021_deprivation_oa.csv')
except:
  deprivation_oa = pd.read_csv('https://www.nomisweb.co.uk/api/v01/dataset/NM_2031_1.data.csv?date=latest&geography=629165479...629165982,629303674...629303812,629317322...629317326,629317336...629317343,629317349...629317360,629317362...629317366,629317371,629317374,629317376,629317378,629317379,629317381,629317385,629317388...629317392,629317394...629317397,629317399...629317403,629317405...629317407,629317409,629317411,629317412,629317416...629317420,629317422...629317424,629317426,629317429...629317434,629317436,629317437,629317440...629317442,629317444...629317450,629317452...629317456,629317459...629317461,629317463,629317466...629317468,629317472,629317474...629317479,629317481,629317483,629317486,629317487,629317490,629317492,629317494,629317495,629317497,629317499...629317502,629317504,629317505,629317507...629317509,629317512...629317514,629317517,629317520,629317523,629317525,629317527,629317531,629317534,629317535,629317537,629317538,629317540,629317543...629317548,629317551,629317554,629317555,629317558,629317560,629317562,629317563,629317565,629317566,629317569...629317573,629317576...629317578,629317580,629317582,629317584,629317585,629317587,629317590...629317592,629317594,629317596...629317599,629317601,629317603,629317604,629317606,629317607,629317610,629317612,629317613,629317615...629317617,629317619...629317621,629317623,629317625...629317629,629317631...629317634,629317636,629317640,629317648,629317650...629317659,629317662,629317663,629317666...629317669,629317672...629317687,629317689,629317691,629317694,629317695,629317697,629317698,629317700,629317701,629317703,629317704,629317706,629317707,629317711...629317714,629317716,629317718...629317720,629317722...629317724,629317726,629317729,629317731,629317733,629317736...629317742,629317744,629317746...629317748,629323624,629323625&c2021_dep_6=0,5&measures=20100,20301&select=date_name,geography_name,geography_code,c2021_dep_6_name,measures_name,obs_value,obs_status_name')
  deprivation_oa.to_csv('lbth_census_2021_deprivation_oa.csv')

# %%
deprivation_merge=merge_spatial_data(oa21, deprivation_oa,"OA21CD", "GEOGRAPHY_CODE")

# %%
deprivation_wd_oa_merged= deprivation_merge.merge(wd_oa_lkup, left_on='OA21CD', right_on='oa21cd')

# %% [markdown]
# Multi-variable dashboard
# ==

# %%
st.set_page_config(layout = "wide")
st.header("Ward profiles")

page = st.sidebar.selectbox('Select variable',
  ['Population density','Deprived in 4 dimensions'])

if page == 'Population density':
  
  #MAKE PLOTY MAP OF POPULATION DENSITY BT WARD

 fig = px.choropleth(popden_wd_oa_merged.dissolve(by='ward_name'),
                   geojson=popden_wd_oa_merged.dissolve(by='ward_name').geometry,
                   locations=popden_wd_oa_merged.dissolve(by='ward_name').index,
                   color="OBS_VALUE",
                   color_continuous_scale = 'viridis_r',
                   projection="mercator",
                   hover_name=popden_wd_oa_merged.dissolve(by='ward_name').index,
                   hover_data=['OBS_VALUE'])
 fig.update_geos(fitbounds="locations", visible=False)
 st.plotly_chart(fig,use_container_width = True)
    
else: 
 fig = px.choropleth(deprivation_wd_oa_merged.dissolve(by='ward_name'),
                   geojson=popden_wd_oa_merged.dissolve(by='ward_name').geometry,
                   locations=popden_wd_oa_merged.dissolve(by='ward_name').index,
                   color="OBS_VALUE",
                   color_continuous_scale = 'viridis_r',
                   projection="mercator",
                   hover_name=deprivation_wd_oa_merged.dissolve(by='ward_name').index,
                   hover_data=['OBS_VALUE'])
 fig.update_geos(fitbounds="locations", visible=False)
 st.plotly_chart(fig,use_container_width = True)


