import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-us')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

def recommend(movie):
    # Load movies_list and similarity here
    movies_list = pickle.load(open('movies.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))

    # Find the index of the given movie in movies_list
    movie_index = movies_list[movies_list["title"] == movie].index
    if len(movie_index) == 0:
        st.write(f"{movie} not found in the DataFrame.")
        return [], []

    movie_index = movie_index[0]

    # Calculate similarity scores
    distances = similarity[movie_index]

    # Sort the movies based on similarity and select the top 5
    movie_indices = sorted(range(len(distances)), reverse=True, key=lambda x: distances[x])[1:6]

    # Print the titles of recommended movies
    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_indices:
        movie_id = movies_list.iloc[i]["movie_id"]  # Use the correct column name for movie ID

        recommended_movies.append(movies_list.iloc[i]["title"])
        # Fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Load movies_list and similarity here
movies_list = pickle.load(open('movies.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie:',
    movies_list['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    columns = st.columns(5)
    for i in range(5):
        with columns[i]:
            st.header(names[i])
            st.image(posters[i])
