import streamlit as st
import pandas as pd
import random

# Load combined dataset
data_url_english = "/mnt/data/english_movie.csv"
data_url_indian = "/mnt/data/indian_movies.csv"

# Load datasets
english_movies = pd.read_csv(data_url_english)
indian_movies = pd.read_csv(data_url_indian)

# Clean and merge datasets
indian_movies.replace("-", pd.NA, inplace=True)
indian_movies.rename(columns={
    "Movie Name": "title",
    "Language": "original_language",
    "Genre": "genres",
    "Rating(10)": "vote_average",
    "Timing(min)": "runtime"
}, inplace=True)

indian_movies["vote_average"] = pd.to_numeric(indian_movies["vote_average"], errors="coerce")
indian_movies["runtime"] = indian_movies["runtime"].astype(str).str.replace(" min", "", regex=True)
indian_movies["runtime"] = pd.to_numeric(indian_movies["runtime"], errors="coerce")

language_map = {
    "hindi": "hi",
    "tamil": "ta",
    "telugu": "te",
    "malayalam": "ml"
}
indian_movies["original_language"] = indian_movies["original_language"].str.lower().map(language_map)

indian_movies = indian_movies[["title", "original_language", "genres", "vote_average", "runtime"]]
english_movies = english_movies[["title", "original_language", "genres", "vote_average", "runtime"]]

combined_movies = pd.concat([english_movies, indian_movies], ignore_index=True)

st.title("🎬 Smart Movie Recommender")
st.write("Answer a few questions, and we'll suggest the perfect movie for you! 🎥")

# Step 1: Ask for language preference
language = st.selectbox("What language are you in the mood for?", ["English", "Hindi", "Tamil", "Telugu", "Malayalam"])

# Map language input to dataset language codes
language_map_reverse = {"English": "en", "Hindi": "hi", "Tamil": "ta", "Telugu": "te", "Malayalam": "ml"}
language_code = language_map_reverse[language]

# Step 2: Ask for genre preference
genre = st.selectbox("Which genre do you feel like watching?", ["Action", "Comedy", "Drama", "Horror", "Sci-Fi", "Romance", "Adventure"])

# Step 3: General fun questions
mood = st.radio("What's your mood today?", ["Excited", "Chill", "Emotional", "Adventurous"])
time_available = st.selectbox("How much time do you have?", ["Short (Under 1.5 hours)", "Medium (1.5-2.5 hours)", "Long (Over 2.5 hours)"])

# Step 4: Filter movies based on preferences
filtered_movies = combined_movies[(combined_movies['original_language'] == language_code) & (combined_movies['genres'].str.contains(genre, na=False))]

if not filtered_movies.empty:
    suggested_movie = random.choice(filtered_movies['title'].dropna().tolist())
    st.success(f"We recommend you to watch: 🎬 **{suggested_movie}**")
else:
    st.error("Sorry, we couldn't find a perfect match. Try changing your preferences!")
