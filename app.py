import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmMjYxMTQ1MjdmNjBmZGMwNmEyNWIwNWNmMGY3ZGFlYyIsInN1YiI6IjY0ODg1MmYzOTkyNTljMDEzOTJjZjQ5ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.56tNnEA7waqnpVlHIBH3f9PvHRnkIvj4Dn-mwMsTI_A"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    similar_movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie_list = []
    recommended_movie_poster = []
    for i in similar_movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movie_list.append(movies.iloc[i[0]].title)
        recommended_movie_poster.append(fetch_poster(movie_id))  # fetch poster from API
    return recommended_movie_list, recommended_movie_poster


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender')

selected_movie_name = st.selectbox(
    'Choose your favorite movie',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
