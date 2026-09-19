import geopandas as gpd
import pandas as pd

def load_geojson(path: str, crs: str = "EPSG:4326") -> gpd.GeoDataFrame:
    gdf = gpd.read_file(path)
    if gdf.crs is None:
        gdf.set_crs(crs, inplace=True)
    return gdf

def load_csv_points(path: str, lat_col: str = "lat", lon_col: str = "lon", crs: str = "EPSG:4326") -> gpd.GeoDataFrame:
    df = pd.read_csv(path)
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[lon_col], df[lat_col]), crs=crs)
    return gdf
