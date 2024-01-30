import streamlit as st
import folium
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import wikipediaapi
import re
import geopandas as gpd
from shapely.geometry import Point


# Load GeoJSON from a URL or a local file path
url = r'https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json'
# For a local file, replace the URL with the file path
# e.g., 'path_to_your_file/us_states.geojson'

gdf = gpd.read_file(url)

# Check the GeoDataFrame
print(gdf.head())

def determine_state_from_lat_lon(lat, lon):
    point = Point(lon, lat)
    for _, row in gdf.iterrows():
        if row['geometry'].contains(point):
            return row['name']  # Assuming the column with state names is 'NAME'
    return "Unknown"

# Example usage
state = determine_state_from_lat_lon(40.7128, -74.0060)  # Example coordinates for New York
print(state)

# # Function to fetch top words from Wikipedia
# def get_top_words_from_wikipedia(state):
#     wiki_wiki = wikipediaapi.Wikipedia('en')
#     page = wiki_wiki.page(state)

#     # Extracting words and filtering
#     words = re.findall(r'\b\w+\b', page.text.lower())
#     return ' '.join(words[:10000])  # Limiting to top 10000 words

# # Function to generate word cloud in the shape of the state
# def generate_state_word_cloud(words, state_mask):
#     mask = np.array(Image.open(state_mask))
#     wordcloud = WordCloud(width = 800, height = 400, background_color ='white', mask=mask, contour_width=1, contour_color='steelblue').generate(words)
#     plt.figure(figsize = (8, 8), facecolor = None) 
#     plt.imshow(wordcloud, interpolation="bilinear") 
#     plt.axis("off")
#     plt.tight_layout(pad = 0) 
#     plt.close()
#     return wordcloud.to_image()

# # Streamlit app
# st.title('US States Interactive Map and Word Clouds')

# # Folium map setup
# m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

# # Streamlit: Display map
# map_data = st_folium(m, width=700)

# # Check if a location is clicked on the map
# if map_data['last_clicked']:
#     lat, lon = map_data['last_clicked']
#     # You need a function to determine the state based on lat, lon
#     # state = determine_state_from_lat_lon(lat, lon)
#     state



