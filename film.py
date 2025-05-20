#%% Importe
import pandas as pd
import json
import streamlit as st
from PIL import Image
import requests
from io import BytesIO

#%% JSON-Datei einlesen
with open('top250-movies.json', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Nur jede zweite Zeile enthält die eigentlichen Filmdaten
movie_data = [json.loads(lines[i]) for i in range(1, len(lines), 2)]

# In DataFrame umwandeln
df = pd.DataFrame(movie_data)

#%% Streamlit App

# App-Titel
st.title("🎬 Top 250 Movies Explorer")

# Dinosaurier-Bild anzeigen (für Dino 🦖)
image_url = "https://upload.wikimedia.org/wikipedia/commons/6/6e/Tyrannosaurus_BW.jpg"  # Beispielbild
response = requests.get(image_url)
img = Image.open(BytesIO(response.content))
st.image(img, caption="Für Dino 🦖", use_column_width=True)

# Seitenleiste für Filter
st.sidebar.header("🔍 Filter")

# Filter: Genre
all_genres = sorted({genre for genres in df["genres"] for genre in genres})
selected_genres = st.sidebar.multiselect("Genre auswählen:", all_genres)

# Filter: Mindestbewertung
min_rating = st.sidebar.slider("Minimale Bewertung", 0.0, 10.0, 8.5, 0.1)

# Filter anwenden
filtered_df = df[
    (df['rating'] >= min_rating) &
    (df['genres'].apply(lambda g: any(genre in g for genre in selected_genres) if selected_genres else True))
]

# Ergebnisse anzeigen
st.markdown(f"### 🎞️ Gefundene Filme für Dino: {len(filtered_df)}")
st.dataframe(filtered_df[['title', 'year', 'rating', 'genres', 'votes', 'languages']])

