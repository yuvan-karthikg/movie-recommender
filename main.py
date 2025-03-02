import streamlit as st
import pandas as pd
import random

# Load combined dataset
data_url_english = "https://raw.githubusercontent.com/yuvan-karthikg/movie-recommender/refs/heads/main/english_movie.csv"
data_url_indian = "https://raw.githubusercontent.com/yuvan-karthikg/movie-recommender/refs/heads/main/indian_movies.csv"

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

indian_movies.rename(columns={"Year": "release_year"}, inplace=True)
indian_movies = indian_movies[["title", "original_language", "genres", "vote_average", "runtime", "release_year"]]
english_movies["release_year"] = pd.to_datetime(english_movies["release_date"], errors='coerce').dt.year
english_movies = english_movies[["title", "original_language", "genres", "vote_average", "runtime", "release_year"]]

combined_movies = pd.concat([english_movies, indian_movies], ignore_index=True)

# Ensure release_year is numeric
combined_movies["release_year"] = pd.to_numeric(combined_movies["release_year"], errors='coerce')

st.title("🎬 Smart Movie Recommender")
st.write("Answer a few questions, and we'll suggest the perfect movie for you! 🎥")

# Step 1: Ask for language preference
language = st.selectbox("What language are you in the mood for?", ["English", "Hindi", "Tamil", "Telugu", "Malayalam"])

# Map language input to dataset language codes
language_map_reverse = {"English": "en", "Hindi": "hi", "Tamil": "ta", "Telugu": "te", "Malayalam": "ml"}
language_code = language_map_reverse[language]

# Step 2: Ask for genre preference
genre = st.selectbox("Which genre do you feel like watching?", ["Action", "Comedy", "Drama", "Horror", "Sci-Fi", "Romance", "Adventure"])

# Step 3: Ask for year and duration preference
year_of_release = st.radio("Which year range do you prefer?", ["Before 2000", "2000-2010", "After 2010"])
time_available = st.selectbox("How much time do you have?", ["Under 1.5 hours", "1.5 - 3 hours", "Above 3 hours"])

# Step 4: Filter movies based on preferences
filtered_movies = combined_movies[(combined_movies['original_language'] == language_code) & (combined_movies['genres'].str.contains(genre, na=False))]

# Apply year filter
if year_of_release == "Before 2000":
    filtered_movies = filtered_movies[filtered_movies["release_year"] < 2000]
elif year_of_release == "2000-2010":
    filtered_movies = filtered_movies[(filtered_movies["release_year"] >= 2000) & (filtered_movies["release_year"] <= 2010)]
elif year_of_release == "After 2010":
    filtered_movies = filtered_movies[filtered_movies["release_year"] > 2010]

# Apply duration filter
if time_available == "Under 1.5 hours":
    filtered_movies = filtered_movies[filtered_movies["runtime"] < 90]
elif time_available == "1.5 - 3 hours":
    filtered_movies = filtered_movies[(filtered_movies["runtime"] >= 90) & (filtered_movies["runtime"] <= 180)]
elif time_available == "Above 3 hours":
    filtered_movies = filtered_movies[filtered_movies["runtime"] > 180]

if not filtered_movies.empty:
    suggested_movies = random.sample(filtered_movies['title'].dropna().tolist(), min(3, len(filtered_movies)))
    st.success("We recommend you to watch:")
    for movie in suggested_movies:
        st.write(f"🎬 **{movie}**")
else:
    st.error("Sorry, we couldn't find a perfect match. Try changing your preferences!")
