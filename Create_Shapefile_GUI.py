import streamlit as st
import folium
from streamlit_folium import folium_static
import geopandas as gpd
from shapely.geometry import shape
import json
import os

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

def save_geojson_to_shapefile(geojson, filename='drawn_polygon.shp'):
    if geojson:
        geom = shape(geojson['geometry'])
        gdf = gpd.GeoDataFrame(index=[0], geometry=[geom], crs="EPSG:4326")
        gdf.to_file(filename)
        return filename
    return None

# Streamlit layout
st.title('Draw a Polygon and Export as Shapefile')

# Initialize the Folium map with specified width and height
m = folium.Map(location=[45.5236, -122.6750], zoom_start=13)
draw = folium.plugins.Draw(export=True)
draw.add_to(m)

# Display the map with injected JavaScript for capturing draw events
folium_static(m)
st.markdown(inject_javascript(), unsafe_allow_html=True)

# Handle the GeoJSON data when the button is clicked
geojson_data = st.session_state.get("geojson", None)
if st.button('Save Polygon'):
    if geojson_data:
        filename = save_geojson_to_shapefile(json.loads(geojson_data))
        if filename:
            with open(filename, 'rb') as file:
                btn = st.download_button(
                    label="Download Shapefile",
                    data=file,
                    file_name=filename,
                    mime='application/zip'
                )
            # Clean up the generated shapefiles after serving them
            for ext in ['.shp', '.shx', '.dbf', '.prj', '.cpg']:
                os.remove(filename[:-4] + ext)

# Listener for frontend events (the map drawing)
st.components.v1.html("""<script>
    window.addEventListener('message', event => {
        if (event.data.hasOwnProperty('geojson')) {
            const geojson = JSON.stringify(event.data.geojson);
            window.parent.postMessage({setSessionState: {geojson: geojson}}, '*');
        }
    });
</script>""", height=0, scrolling=False)
