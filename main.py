import streamlit as st
import pandas as pd
import random

# Load datasets
english_movies = pd.read_csv('/mnt/data/english_movie.csv')
indian_movies = pd.read_csv('/mnt/data/indian_movie.csv')

# Function to recommend a movie
def recommend_movie(language, genre, min_year, min_rating):
    if language == 'English':
        movies = english_movies
    else:
        movies = indian_movies[indian_movies['Language'] == language]
    
    # Filter based on user preferences
    filtered_movies = movies[(movies['Genre'].str.contains(genre, case=False, na=False)) &
                              (movies['Year'] >= min_year) &
                              (movies['Rating'] >= min_rating)]
    
    if not filtered_movies.empty:
        return filtered_movies.sample(1).iloc[0]
    else:
        return None

# Streamlit UI
st.title("Movie Recommendation System")

# User input
language = st.radio("What language are you in the mood for?", ["English", "Hindi", "Malayalam", "Tamil", "Telugu"])
genre = st.selectbox("Pick a genre", ["Action", "Comedy", "Drama", "Thriller", "Romance", "Horror"])
min_year = st.slider("Select the minimum release year", min_value=1950, max_value=2025, value=2000)
min_rating = st.slider("Minimum IMDb rating", min_value=0.0, max_value=10.0, value=6.0, step=0.1)

if st.button("Recommend a Movie"):
    movie = recommend_movie(language, genre, min_year, min_rating)
    if movie is not None:
        st.write(f"### {movie['Title']} ({movie['Year']})")
        st.write(f"**Genre:** {movie['Genre']}")
        st.write(f"**IMDb Rating:** {movie['Rating']}")
        st.write(f"**Summary:** {movie.get('Summary', 'No summary available.')}")
    else:
        st.write("No movies found matching your criteria. Try adjusting the filters!")

# Run this script using: streamlit run script_name.py

