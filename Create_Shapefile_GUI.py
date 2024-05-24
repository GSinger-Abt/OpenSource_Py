import streamlit as st
from streamlit.components.v1 import html
from streamlit_js_eval import streamlit_js_eval

# Define the HTML content
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Reverse Geocode Sample</title>
    <meta name="viewport" content="initial-scale=1, maximum-scale=1, user-scalable=no">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin="">
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>
    <!-- Load Esri Leaflet from CDN -->
    <script src="https://unpkg.com/esri-leaflet@3.0.12/dist/esri-leaflet.js"></script>
    <!-- Load Esri Leaflet Geocoder from CDN -->
    <link rel="stylesheet" href="https://unpkg.com/esri-leaflet-geocoder@3.1.4/dist/esri-leaflet-geocoder.css" crossorigin="">
    <script src="https://unpkg.com/esri-leaflet-geocoder@3.1.4/dist/esri-leaflet-geocoder.js" crossorigin=""></script>
    <style>
        html, body {
            padding: 0;
            margin: 0;
            height: 100%;
            width: 100%;
            font-family: Arial, Helvetica, sans-serif;
            font-size: 14px;
            color: #e0e0e0;
            background-color: #2b2b2b;
        }
        #map {
            height: 70%;
            width: 100%;
        }
        .title-container {
            text-align: center;
            margin: 20px 0;
            color: #e0e0e0;
        }
    </style>
</head>
<body>
    <div class="title-container">
        <h1>Reverse Geocode Sample</h1>
    </div>
    <div id="map"></div>
    <script>
        const apiKey = "AAPK3f380629777b492f98ca73660d2b389eEfJGfm-x5DSEsz1W_tWvWvRgbWaOn1GxLdNQe8fvMsI3bRGHAlcpC-4d-Zvcqm6S";

        const map = L.map("map").setView([40.725, -73.985], 13);

        L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", {
            attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ',
            maxZoom: 23
        }).addTo(map);

      L.tileLayer("https://services.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}", {
            attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ',
            maxZoom: 23
        }).addTo(map);

        // Add the search control
        const searchControl = L.esri.Geocoding.geosearch({
            position: 'topright',
            useMapBounds: false,
            placeholder: 'Search for an address',
            providers: [
                L.esri.Geocoding.arcgisOnlineProvider({
                    apikey: apiKey,
                    nearby: {
                        lat: 40.725,
                        lng: -73.985
                    }
                })
            ]
        }).addTo(map);

        const results = L.layerGroup().addTo(map);
        let marker;

        searchControl.on('results', function(data) {
            results.clearLayers();
            if (marker) {
                map.removeLayer(marker);
            }
            for (let i = data.results.length - 1; i >= 0; i--) {
                marker = L.marker(data.results[i].latlng).addTo(map).bindPopup(data.results[i].text).openPopup();
                
                const locationData = {
                    longitude: data.results[i].latlng.lng.toFixed(6),
                    latitude: data.results[i].latlng.lat.toFixed(6),
                    city: data.results[i].properties.City || '',
                    state: data.results[i].properties.Region || '',
                    country: data.results[i].properties.CntryName || ''
                };
                const jsonData = JSON.stringify(locationData);
                console.log(jsonData); // For debugging

                // Pass the data back to Streamlit
                parent.postMessage({ isStreamlitMessage: true, type: 'reverseGeocodeData', data: jsonData }, '*');
            }
        });

        map.on("click", function (e) {
            if (marker) {
                map.removeLayer(marker);
            }
            L.esri.Geocoding.reverseGeocode({
                apikey: apiKey
            })
            .latlng(e.latlng)
            .run(function (error, result) {
                if (error) {
                    console.error(error);
                    return;
                }

                marker = L.marker(result.latlng).addTo(map).bindPopup(result.address.Match_addr).openPopup();

                const locationData = {
                    longitude: result.latlng.lng.toFixed(6),
                    latitude: result.latlng.lat.toFixed(6),
                    city: result.address.City || '',
                    state: result.address.Region || '',
                    country: result.address.CntryName || ''
                };
                const jsonData = JSON.stringify(locationData);
                console.log(jsonData); // For debugging

                // Pass the data back to Streamlit
                parent.postMessage({ isStreamlitMessage: true, type: 'reverseGeocodeData', data: jsonData }, '*');
            });
        });
    </script>
</body>
</html>
"""

# Inject the HTML into Streamlit app
st.title("Reverse Geocode Sample")
st.markdown("This is a reverse geocoding sample integrated with Streamlit.")
result = html(html_content, height=700)

# Define placeholders for displaying data
longitude = st.text_input("Longitude", "")
latitude = st.text_input("Latitude", "")
city = st.text_input("City", "")
state = st.text_input("State", "")
country = st.text_input("Country", "")

# JavaScript to handle messages from iframe
js_code = """
<script>
window.addEventListener('message', (event) => {
    if (event.data && event.data.isStreamlitMessage && event.data.type === 'reverseGeocodeData') {
        const data = JSON.parse(event.data.data);
        window.parent.postMessage({
            isStreamlitMessage: true,
            type: 'updateInputs',
            data: data
        }, '*');
    }
});
</script>
"""
st.components.v1.html(js_code, height=0)

# Use streamlit_js_eval to handle the communication
location_data = streamlit_js_eval('document.getElementById("map").contentWindow.data', target="reverseGeocodeData")

if location_data:
    st.text_input("Longitude", location_data.get('longitude', ''))
    st.text_input("Latitude", location_data.get('latitude', ''))
    st.text_input("City", location_data.get('city', ''))
    st.text_input("State", location_data.get('state', ''))
    st.text_input("Country", location_data.get('country', ''))

   




# import streamlit as st
# import folium
# from streamlit_folium import folium_static
# import geopandas as gpd
# from shapely.geometry import shape
# import json
# import os

# def inject_javascript():
#     js = """
#     <script>
#         var map = window.folium_vars.maps[0];
#         function handleMapEvent(e) {
#             var geojsonData = e.layer.toGeoJSON();
#             window.parent.postMessage({geojson: geojsonData}, '*');
#         }
#         map.on('draw:created', handleMapEvent);
#     </script>
#     """
#     return js

# def save_geojson_to_shapefile(geojson, filename='drawn_polygon'):
#     if geojson:
#         geom = shape(geojson['geometry'])
#         gdf = gpd.GeoDataFrame(index=[0], geometry=[geom], crs="EPSG:4326")
#         gdf.to_file(f"{filename}.shp")
#         return f"{filename}.shp"
#     return None

# # Initialize the Folium map with specified width and height
# m = folium.Map(location=[45.5236, -122.6750], zoom_start=13)
# draw = folium.plugins.Draw(export=True)
# draw.add_to(m)

# # Display the map with injected JavaScript for capturing draw events
# folium_static(m)
# st.markdown(inject_javascript(), unsafe_allow_html=True)

# # Listener for frontend events (the map drawing)
# st.components.v1.html("""<script>
#     window.addEventListener('message', event => {
#         if (event.data.hasOwnProperty('geojson')) {
#             const geojson = JSON.stringify(event.data.geojson);
#             window.parent.postMessage({setSessionState: {geojson: geojson}}, '*');
#         }
#     });
# </script>""", height=0, scrolling=False)

# # Button to save the drawn polygon
# if st.button('Save Polygon'):
#     geojson_data = st.session_state.get("geojson", None)
#     if geojson_data:
#         filename = save_geojson_to_shapefile(json.loads(geojson_data))
#         st.session_state['filename'] = filename  # Save the filename in the session state

# # Provide a download button only if the file has been created and stored in session state
# if 'filename' in st.session_state and st.session_state['filename'] is not None:
#     with open(st.session_state['filename'], 'rb') as file:
#         st.download_button(
#             label="Download Shapefile",
#             data=file,
#             file_name=os.path.basename(st.session_state['filename']),
#             mime='application/zip'
#         )

# # Ensure cleanup is managed correctly
# if 'filename' in st.session_state and st.session_state['filename'] is not None:
#     for ext in ['.shp', '.shx', '.dbf', '.prj', '.cpg']:
#         os.remove(st.session_state['filename'][:-4] + ext)
#     del st.session_state['filename']  # Remove the filename from session state after cleanup
