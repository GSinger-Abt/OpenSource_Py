import streamlit as st
import geopandas as gpd
from shapely.geometry import Polygon
from streamlit_folium import folium_static
import folium
import os

def save_polygon(shape, filename='output_polygon'):
    """Save the polygon shape to a shapefile."""
    # Create a GeoDataFrame
    gdf = gpd.GeoDataFrame(index=[0], crs='epsg:4326', geometry=[shape])
    # Save the GeoDataFrame to a Shapefile
    gdf.to_file(f"{filename}.shp")

# Streamlit interface
st.title('Draw and Download Shapefile Polygon')

# Initialize Folium map
m = folium.Map(location=[45.5236, -122.6750], zoom_start=13, control_scale=True)
# Add draw tools to the map
draw = folium.plugins.Draw(
    draw_options={
        'polyline':False,
        'rectangle':False,
        'circle':False,
        'circlemarker':False,
    },
    edit_options={'edit':False}
)
draw.add_to(m)

# Display the map
folium_static(m)

# Button to download the shapefile
if st.button('Save Polygon'):
    # Retrieve geojson data from draw control
    draw_data = draw.last_draw
    if draw_data:
        shape_type = draw_data['geometry']['type']
        if shape_type == 'Polygon':
            coordinates = draw_data['geometry']['coordinates'][0]
            polygon = Polygon(coordinates)
            save_polygon(polygon)
            with open('output_polygon.shp', 'rb') as f:
                st.download_button('Download Shapefile', f, file_name='polygon_shapefile.shp')

# Clean up files (optional)
if os.path.exists('output_polygon.shp'):
    os.remove('output_polygon.shp')
    os.remove('output_polygon.cpg')
    os.remove('output_polygon.dbf')
    os.remove('output_polygon.prj')
    os.remove('output_polygon.shx')

