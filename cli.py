from pathlib import Path
import geopandas as gpd
import pandas as pd
from .utils.config import load_config
from .utils.logging import get_logger
from .data_ingest import load_geojson, load_csv_points
from .processing import build_features

def main():
    log = get_logger()
    cfg = load_config("config.yaml")
    log.info("Loading data...")
    rivers = load_geojson(cfg["files"]["rivers"], crs=cfg["crs_input"])
    boundary = load_geojson(cfg["files"]["boundary"], crs=cfg["crs_input"])
    hospitals = load_csv_points(cfg["files"]["hospitals"], crs=cfg["crs_input"])
    population = load_csv_points(cfg["files"]["population"], crs=cfg["crs_input"])
    rainfall = load_csv_points(cfg["files"]["rainfall"], crs=cfg["crs_input"])

    log.info("Building features and risk scoring...")
    risk_gdf = build_features(population, rainfall, rivers, hospitals, cfg, boundary)

    out_geojson = Path(cfg["outputs"]["risk_geojson"]).as_posix()
    out_csv = Path(cfg["outputs"]["summary_csv"]).as_posix()
    Path(out_geojson).parent.mkdir(parents=True, exist_ok=True)

    log.info(f"Writing outputs: {out_geojson} and {out_csv}")
    risk_gdf.to_file(out_geojson, driver="GeoJSON")
    risk_gdf.drop(columns=["geometry"]).to_csv(out_csv, index=False)

    log.info("Done. Load outputs in QGIS or open the Streamlit dashboard.")

if __name__ == "__main__":
    main()


