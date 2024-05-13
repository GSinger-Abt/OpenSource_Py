import streamlit as st
import folium
from streamlit_folium import folium_static
import geopandas as gpd
from shapely.geometry import shape
import json

st.title('Draw a Polygon and Export as Shapefile')

# Initialize the map:
m = folium.Map(location=[45.5236, -122.6750], zoom_start=13)
draw = folium.plugins.Draw(
    export=True,
    filename='data.geojson',
    position='topleft',
    draw_options={'polygon': True},
    edit_options={'edit': True}
)
draw.add_to(m)

# Display the map:
folium_static(m)

# Input for GeoJSON data
geojson_input = st.text_area("Paste the GeoJSON here:")

# Button to save the drawn polygon
if st.button('Save Polygon') and geojson_input:
    geojson = json.loads(geojson_input)
    geom = shape(geojson['geometry'])
    gdf = gpd.GeoDataFrame(index=[0], geometry=[geom], crs="EPSG:4326")
    gdf.to_file("drawn_polygon.shp")
    st.success("Shapefile saved!")


