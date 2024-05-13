import streamlit as st
import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon
import pydeck as pdk

# Function to create and save the polygon shapefile
def save_polygon(coords_list, filename='output_polygon'):
    polygon = Polygon(coords_list)  # Create the polygon from the coords list
    gdf = gpd.GeoDataFrame(index=[0], crs='epsg:4326', geometry=[polygon])  # Create a GeoDataFrame
    gdf.to_file(filename + ".shp")  # Save to a Shapefile

# Streamlit UI
st.title("Draw a Polygon and Download as Shapefile")

# User inputs for polygon vertices
coords_input = st.text_area("Enter polygon coordinates as a list of tuples (e.g., [(0,0), (1,1), (1,0)])", "[(0,0), (1,1), (1,0)]")
coords = eval(coords_input)

# Convert coordinates to a DataFrame
df = pd.DataFrame(coords, columns=['lng', 'lat'])

# Create a PyDeck map to display the polygon
layer = pdk.Layer(
    'PolygonLayer',  # The type of layer to render
    df,  # The DataFrame containing the polygon data
    get_polygon='coordinates',  # The accessor that returns polygon coordinates
    get_fill_color=[255, 0, 0, 100],  # Set the fill color to red with some transparency
)

view_state = pdk.ViewState(
    latitude=df['lat'].mean(),  # Center the map around the polygon
    longitude=df['lng'].mean(),
    zoom=10,
    pitch=0,
)

# Render PyDeck map
r = pdk.Deck(layers=[layer], initial_view_state=view_state, map_provider="mapbox", map_style=pdk.map_styles.SATELLITE)
st.pydeck_chart(r)

# Button to create and download shapefile
if st.button('Create and Download Shapefile'):
    save_polygon(coords)
    with open('output_polygon.shp', 'rb') as f:
        st.download_button('Download Shapefile', f, file_name='polygon_shapefile.shp')

