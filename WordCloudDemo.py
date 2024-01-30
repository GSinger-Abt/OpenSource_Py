import streamlit as st
import requests
import folium
from streamlit_folium import folium_static
from bs4 import BeautifulSoup
from collections import Counter
import nltk
nltk.download('punkt')

# Function to load GeoJSON data
def load_geojson(url):
    return requests.get(url).json()

# Function to scrape Wikipedia and analyze text
def analyze_state_wiki(state_name):
    wiki_url = f'https://en.wikipedia.org/wiki/{state_name}_State'
    response = requests.get(wiki_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()
    words = nltk.word_tokenize(text)
    frequent_words = Counter(words).most_common(10)  # Adjust the number as needed
    return frequent_words

# Streamlit App
def main():
    st.title('US States Word Frequency Analyzer')
    
    # Load and display the map for state selection
    geojson_data = load_geojson('https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json')
    
    # Creating the map (Example with folium - You may need to adjust it based on your exact requirements)
    m = folium.Map(location=[48, -102], zoom_start=3)
    folium.GeoJson(geojson_data).add_to(m)
    folium_static(m)

    # Input for state name (You might want to replace this with a more sophisticated state selection method)
    state_name = st.text_input('Enter a State Name')

    if state_name:
        frequent_words = analyze_state_wiki(state_name)
        st.write(f'Most Frequent Words in {state_name} Wikipedia Page:')
        st.write(frequent_words)

if __name__ == "__main__":
    main()


