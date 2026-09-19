# Flood Risk Intelligence (QGIS + Python + Streamlit)

A richer, end-to-end GIS project that simulates **flood risk analysis** using open tooling.
It includes synthetic datasets, a Python processing pipeline (GeoPandas/Shapely), a Streamlit
dashboard for interactive maps, and a simple unit test.

## Highlights
- **Ingest → Process → Model → Visualize** pipeline
- Distance-to-river/hospital and rainfall/population risk features
- Streamlit dashboard with interactive map layers
- Config-driven (YAML) and CLI to run the pipeline
- QGIS-friendly GeoJSON outputs (load `outputs/risk_zones.geojson` in QGIS)

## Project Structure
```
GIS_FloodRisk_Advanced/
├── data/
│   └── synthetic/                 # synthetic demo datasets
├── outputs/                       # generated artifacts
├── notebooks/
│   └── 01_exploration.ipynb       # (placeholder) exploration notebook
├── src/
│   ├── cli.py                     # CLI to run end-to-end pipeline
│   ├── data_ingest.py             # loaders for CSV/GeoJSON
│   ├── processing.py              # geospatial feature engineering
│   ├── risk_model.py              # risk scoring + classification
│   ├── utils/
│   │   ├── config.py              # YAML config loader
│   │   └── logging.py             # simple logger
│   └── viz/
│       └── dashboard.py           # Streamlit app
├── tests/
│   └── test_risk_model.py         # unit tests
├── config.yaml                    # project configuration
└── requirements.txt               # dependencies
```

## Quickstart

> Python 3.10+ recommended. Use a virtual env.

```bash
pip install -r requirements.txt

# run the pipeline (reads config.yaml)
python -m src.cli

# launch the dashboard
streamlit run src/viz/dashboard.py
```

### Open in QGIS
- Open QGIS → Add Vector Layer → `outputs/risk_zones.geojson`.
- Style by `risk_class` or `risk_score`.
- You can also load `data/synthetic/rivers.geojson` and `data/synthetic/hospitals.csv` (as delimited text layer).

## Notes
- Data are synthetic and small so you can run quickly offline.
- Replace `data/synthetic` with real rasters/shapefiles and it still works (GeoJSON/CSV friendly).
