import streamlit as st
import geopandas as gpd
from shapely.geometry import Polygon
import os

# Function to convert input to polygon and save as shapefile
def create_shapefile(coords_list, filename='output_polygon'):
    # Create the Polygon
    polygon = Polygon(coords_list)
    # Create a GeoDataFrame
    gdf = gpd.GeoDataFrame(index=[0], crs='epsg:4326', geometry=[polygon])
    # Save the GeoDataFrame to a Shapefile
    gdf.to_file(f"{filename}.shp")

# Streamlit interface
st.title('Create and Download Shapefile')

# User input for polygon coordinates
coords_input = st.text_area("Enter polygon coordinates as a list of tuples (e.g., (0,0), (1,1), (1,0))", "[(0,0), (1,1), (1,0)]")
# Convert string input to list of tuples
coords = eval(coords_input)

# Button to create and download shapefile
if st.button('Create Shapefile'):
    create_shapefile(coords)
    with open('output_polygon.shp', 'rb') as f:
        st.download_button('Download Shapefile', f, file_name='polygon_shapefile.shp')

# Clean up files (optional, depending on your use case)
if os.path.exists('output_polygon.shp'):
    os.remove('output_polygon.shp')
    os.remove('output_polygon.cpg')
    os.remove('output_polygon.dbf')
    os.remove('output_polygon.prj')
    os.remove('output_polygon.shx')
