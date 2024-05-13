import streamlit as st
import folium
from streamlit_folium import folium_static
import geopandas as gpd
from shapely.geometry import shape
import json

def inject_javascript():
    js = """
    <script>
        var map = window.folium_vars.maps[0];
        function handleMapEvent(e) {
            var geojsonData = e.layer.toGeoJSON();
            window.parent.postMessage({geojson: geojsonData}, '*');
        }
        map.on('draw:created', handleMapEvent);
    </script>
    """
    return js

def save_geojson_to_shapefile(geojson):
    if geojson:
        geom = shape(geojson['geometry'])
        gdf = gpd.GeoDataFrame(index=[0], geometry=[geom], crs="EPSG:4326")
        gdf.to_file("drawn_polygon.shp")
        return True
    return False

# Streamlit layout
st.title('Draw a Polygon and Export as Shapefile')

# Initialize the Folium map:
m = folium.Map(location=[45.5236, -122.6750], zoom_start=13, width='100%', height='80vh')  # Map taking larger area
draw = folium.plugins.Draw(export=True)
draw.add_to(m)

# Display the map with injected JavaScript for capturing draw events:
folium_static(m)
st.markdown(inject_javascript(), unsafe_allow_html=True)

# Custom CSS to make the button more visible
st.markdown("""
<style>
.big-btn {
    font-size: 20px;
    font-weight: bold;
    color: white;
    background-color: blue;
    padding: 10px 24px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    margin: 10px 0;
}
</style>
<button class="big-btn" onclick="document.getElementById('btn-save').click()">Export Shapefile</button>
""", unsafe_allow_html=True)

# Save button
if st.button('Save Polygon', key='btn-save', help='Click to save the drawn polygon as a shapefile'):
    geojson_data = st.session_state.get("geojson", None)
    if geojson_data and save_geojson_to_shapefile(json.loads(geojson_data)):
        st.success("Shapefile saved!")

# Listener for frontend events (the map drawing)
st.components.v1.html("""<script>
    window.addEventListener('message', event => {
        if (event.data.hasOwnProperty('geojson')) {
            const geojson = JSON.stringify(event.data.geojson);
            window.parent.postMessage({setSessionState: {geojson: geojson}}, '*');
        }
    });
</script>""", height=0, scrolling=False)
