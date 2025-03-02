import streamlit as st
import pandas as pd
import random


df_eng = pd.read_csv("english_movies.csv")
df_indian = pd.read_csv("indian_movies.csv")


df = pd.concat([df_eng, df_indian], ignore_index=True)


df = df[['original_title', 'overview', 'genres', 'original_language']]


def extract_genres(genre_str):
    try:
        import ast  # To safely evaluate the string as a list of dictionaries
        genres = [g['name'] for g in ast.literal_eval(genre_str)]
        return ', '.join(genres)
    except:
        return "Unknown"

df['genres'] = df['genres'].apply(extract_genres)

# Streamlit UI
st.title("🎬 Movie Recommendation System")
st.write("Find the perfect movie based on your preferences!")


language_mapping = {
    'en': 'English',
    'hi': 'Hindi',
    'ta': 'Tamil',
    'ml': 'Malayalam',
    'te': 'Telugu'
}
df['language_full'] = df['original_language'].map(language_mapping).fillna(df['original_language'])

language = st.selectbox("What language are you in the mood for today?", options=df['language_full'].unique())


genre_options = set(', '.join(df['genres'].unique()).split(', '))
genre = st.selectbox("What genre do you prefer?", options=sorted(genre_options))


extra_genres = st.multiselect("Any additional genres you'd like to include?", options=sorted(genre_options))


filtered_movies = df[(df['original_language'] == language) & (df['genres'].str.contains(genre, case=False, na=False))]


if extra_genres:
    for g in extra_genres:
        filtered_movies = filtered_movies[filtered_movies['genres'].str.contains(g, case=False, na=False)]


if not filtered_movies.empty:
    selected_movie = filtered_movies.sample(1).iloc[0]
    st.write("### 🎥 We recommend you watch:")
    st.subheader(selected_movie['original_title'])
    st.write("**Genre:**", selected_movie['genres'])
    st.write("**Overview:**", selected_movie['overview'])
else:
    st.write("❌ Sorry, no movies found matching your criteria. Try adjusting your filters!")
