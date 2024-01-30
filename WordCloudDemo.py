import streamlit as st
import pandas as pd
import plotly.express as px
from urllib.request import urlopen
import json

st.set_page_config(
    page_title='Word Cloud Demo.py',
    page_icon="🗺️",
    layout="wide",
)
st.title('Open Source Word Cloud Demo')
st.subheader("Introduction:")
st.markdown(
    """
    Testing

    ---

    
    """
)

# Load US states geojson
with urlopen('https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json') as response:
    states = json.load(response)

# Sample dataframe
data = {
    'State': ['CA', 'TX', 'NY', 'FL', 'IL'],
    'Value': [100, 200, 300, 400, 500]
}
df = pd.DataFrame(data)

# Function to return filtered dataframe
def filter_data(selected_state):
    return df[df['State'] == selected_state]

# Plotly map
fig = px.choropleth(df, geojson=states, locations='State', locationmode='USA-states', color='Value',
                    scope="usa")
fig.update_geos(fitbounds="locations")

# Streamlit app
st.title('US States Map Click Interaction')

# Display map
map_click = st.plotly_chart(fig, use_container_width=True)

# Get click data
selected_data = map_click._click_data
if selected_data:
    selected_state = selected_data['points'][0]['location']
    filtered_df = filter_data(selected_state)
    st.write(f"Selected state: {selected_state}")
    st.write(filtered_df)
else:
    st.write("Click on a state in the map")

