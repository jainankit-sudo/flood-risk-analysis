import geopandas as gpd
from shapely.geometry import Point
from .risk_model import normalize_series, classify_quantiles

def to_metric(gdf: gpd.GeoDataFrame, metric_crs: str) -> gpd.GeoDataFrame:
    return gdf.to_crs(metric_crs)

def clip_to_boundary(gdf: gpd.GeoDataFrame, boundary: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    return gpd.overlay(gdf, boundary, how="intersection")

def compute_distance_to_nearest(a: gpd.GeoDataFrame, b: gpd.GeoDataFrame, colname: str) -> gpd.GeoDataFrame:
    # Assumes both are in metric CRS
    b_sindex = b.sindex
    nearest = []
    for geom in a.geometry:
        cand_idx = list(b_sindex.nearest(geom.bounds, 1))[0]
        nearest.append(geom.distance(b.iloc[cand_idx].geometry))
    a[colname] = nearest
    return a

def buffer_rivers(rivers: gpd.GeoDataFrame, buffer_m: float) -> gpd.GeoDataFrame:
    buf = rivers.copy()
    buf["geometry"] = rivers.buffer(buffer_m)
    buf["buf_m"] = buffer_m
    return buf

def build_features(pop: gpd.GeoDataFrame, rainfall: gpd.GeoDataFrame, rivers: gpd.GeoDataFrame, hospitals: gpd.GeoDataFrame, cfg: dict, boundary: gpd.GeoDataFrame):
    metric = cfg["crs_metric"]
    # project to metric for distances
    pop_m = to_metric(pop, metric)
    rain_m = to_metric(rainfall, metric)
    riv_m = to_metric(rivers, metric)
    hos_m = to_metric(hospitals, metric)
    bnd_m = to_metric(boundary, metric)

    # clip to boundary
    pop_m = clip_to_boundary(pop_m, bnd_m)
    rain_m = clip_to_boundary(rain_m, bnd_m)

    # spatial join rainfall to population (nearest)
    rain_join = gpd.sjoin_nearest(pop_m, rain_m[["rainfall_mm","geometry"]], how="left", distance_col="rainfall_dist_m")
    # distance to nearest river and hospital
    rain_join = compute_distance_to_nearest(rain_join, riv_m, "dist_river_m")
    rain_join = compute_distance_to_nearest(rain_join, hos_m, "dist_hospital_m")

    # binary river proximity within buffer
    river_prox = (rain_join["dist_river_m"] <= cfg["risk"]["river_buffer_m"]).astype(int)

    # hospital distance penalty (1 if far, else 0)
    hosp_far = (rain_join["dist_hospital_m"] >= cfg["risk"]["hospital_far_m"]).astype(int)

    # normalize rainfall
    rainfall_norm = normalize_series(rain_join["rainfall_mm"])

    w = cfg["risk"]["weights"]
    risk_score = rainfall_norm*w["rainfall"] + river_prox*w["river_proximity"] + hosp_far*w["hospital_distance"]

    out = rain_join.copy()
    out["risk_score"] = risk_score
    out["risk_class"] = classify_quantiles(out["risk_score"], q=5, labels=["Very Low","Low","Moderate","High","Very High"])
    return out[["id","population","rainfall_mm","dist_river_m","dist_hospital_m","risk_score","risk_class","geometry"]]
