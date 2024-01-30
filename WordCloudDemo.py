import streamlit as st
import pandas as pd
import json
import requests
import plotly.express as px
from bs4 import BeautifulSoup
from collections import Counter
import nltk
nltk.download('punkt')

# Load GeoJSON and convert to DataFrame
def load_geojson(url):
    data = requests.get(url).json()
    states = [feature['properties']['name'] for feature in data['features']]
    return pd.DataFrame({'state': states, 'geometry': data['features']})

# Scrape Wikipedia and analyze text
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

    df = load_geojson('https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json')
    
    # Create the Plotly map
    fig = px.choropleth(df, geojson=df['geometry'], locations=df.index, hover_name='state')
    fig.update_geos(fitbounds="locations")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    # Display the map and capture click data
    click_data = st.plotly_chart(fig, use_container_width=True)

    # Handle state selection
    if click_data and click_data['points']:
        selected_state = click_data['points'][0]['location']
        if selected_state:
            st.write(f"Selected State: {selected_state}")
            frequent_words = analyze_state_wiki(selected_state)
            st.write(f'Most Frequent Words in {selected_state} Wikipedia Page:')
            st.write(frequent_words)

if __name__ == "__main__":
    main()


