import geopandas as gpd
import pandas as pd
from pandas import DataFrame
from shapely.geometry import Point

gdf = gpd.read_file("pop_density_data/tl_2020_25_tabblock20.shp")
gdf = gdf.to_crs(epsg=26986)
#print(gdf)

#everything defined by census blocks
#ALAND20 = area in sq m
#INTPTLAT20 = internal lat point
#INTPTLON20 = internal long point
#POP20 = 2020 census population

gdf['POP_DENSITY'] = gdf['POP20'] / gdf['ALAND20']

def weight_csv(csv_name):
    df_311 = pd.read_csv(csv_name)
    
    #convert to GeoDataFrame
    geometry = [Point(lon, lat) for lon, lat in zip(df_311['longitude'], df_311['latitude'])]
    gdf_311 = gpd.GeoDataFrame(df_311, geometry=geometry)
    gdf_311.set_crs(gdf.crs, allow_override=True, inplace=True)
    gdf_311 = gdf_311.to_crs(epsg=26986)

    def find_closest_block(point, gdf):
        distances = gdf.distance(point)
        return distances.idxmin()

    #GeoDataFrame for 311 reports
    gdf_311['block'] = gdf_311.geometry.apply(lambda x: find_closest_block(x, gdf))
    gdf_311['block'] = gdf_311['block'].astype(str)
    print(gdf_311['block'])
    gdf['GEOID20'] = gdf['GEOID20'].astype(str)
    #print(gdf['GEOID20'])
    #join by the block identifier (e.g., GEOID or whatever identifies the census block)
    gdf_311 = gdf_311.merge(gdf[['GEOID20', 'POP_DENSITY']], left_on='block', right_on='GEOID20', how='left')
    #print(gdf_311[gdf_311['POP_DENSITY'].isna()])

    gdf_311.to_csv("pop_weighted_" + csv_name)


if __name__ == "__main__":
    g = 0
    #weight_csv("bc_df_1mile.csv")
    #weight_csv("comparison.csv")
    weight_csv("test_data.csv")

