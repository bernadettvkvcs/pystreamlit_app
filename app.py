import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Cache-elt funkció a jelenlegi időjárás lekéréséhez
@st.cache_data
def get_weather_data(city, api_key):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    
    if data['cod'] != 200:
        st.warning("Hiba történt az adatok lekérésekor. Ellenőrizd a város nevét!")
        return None
    
    return data

# Fő alkalmazás funkció
def main():
    # Alapbeállítások
    st.title("Időjárás és Térkép - OpenWeatherMap")
    
    # API kulcs betöltése a Streamlit titkos kulcsból
    api_key = st.secrets["weather"]["api_key"]
    
    # Város neve - text input a sidebar-ban
    city = st.sidebar.text_input("Add meg a város nevét:", "Budapest")
    
    if city:
        # Jelenlegi időjárás adatainak lekérése
        weather_data = get_weather_data(city, api_key)
        
        if weather_data:
            st.subheader(f"Jelenlegi időjárás a {city} városában")
            # KPI-ok/key metrics megjelenítése
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(label="Hőmérséklet (°C)", value=f"{weather_data['main']['temp']}°C")
            
            with col2:
                st.metric(label="Páratartalom (%)", value=f"{weather_data['main']['humidity']}%")
            
            with col3:
                st.metric(label="Szél sebesség (m/s)", value=f"{weather_data['wind']['speed']} m/s")
            
            # Város koordinátái (lat, lon)
            lat = weather_data['coord']['lat']
            lon = weather_data['coord']['lon']
            
            # Térkép megjelenítése
            st.subheader(f"{city} helye a térképen")
            st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
        
# Az alkalmazás futtatása

    main()