import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from pathlib import Path
import pandas as pd
import json

st.set_page_config(page_title="Flood Risk Intelligence", layout="wide")
st.title("🌊 Flood Risk Intelligence Dashboard")


def load_geojson(path):
    return gpd.read_file(path)

def render_map(risk_path, rivers_path):
    gdf = load_geojson(risk_path)
    rivers = gpd.read_file(rivers_path)

    # center map
    center = [gdf.geometry.y.mean(), gdf.geometry.x.mean()]
    m = folium.Map(location=center, zoom_start=11)

    # add risk points
    folium.GeoJson(
        gdf.to_json(),
        name="Risk Points",
        tooltip=folium.GeoJsonTooltip(fields=["risk_class","risk_score","population","rainfall_mm"], aliases=["Class","Score","Pop","Rain (mm)"]),
        marker=folium.CircleMarker(radius=3)
    ).add_to(m)

    # add rivers
    folium.GeoJson(
        rivers.to_json(),
        name="Rivers",
        style_function=lambda x: {"color":"blue","weight":2}
    ).add_to(m)

    folium.LayerControl().add_to(m)
    return m

risk_geojson = Path("outputs/risk_zones.geojson")
if not risk_geojson.exists():
    st.warning("No outputs found. Run the pipeline first: `python -m src.cli`.")
else:
    m = render_map("outputs/risk_zones.geojson", "data/synthetic/rivers.geojson")
    st_folium(m, width=1200, height=700)

