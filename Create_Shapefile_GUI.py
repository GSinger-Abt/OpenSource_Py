import streamlit as st
import geopandas as gpd
from shapely.geometry import shape
import json

def save_polygon(geojson_str, filename='output_polygon'):
    """Save the polygon shape to a shapefile."""
    geojson = json.loads(geojson_str)
    # Convert GeoJSON to Shapely shape
    shapely_polygon = shape(geojson['geometry'])
    # Create a GeoDataFrame
    gdf = gpd.GeoDataFrame(index=[0], crs='epsg:4326', geometry=[shapely_polygon])
    # Save the GeoDataFrame to a Shapefile
    gdf.to_file(f"{filename}.shp")

# Streamlit interface
st.title('Draw and Download Shapefile Polygon')

geojson_input = st.text_area("Paste the GeoJSON of the drawn polygon here:")
if geojson_input:
    save_polygon(geojson_input)
    with open('output_polygon.shp', 'rb') as f:
        st.download_button('Download Shapefile', f, file_name='polygon_shapefile.shp')
