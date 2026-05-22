from flask import Flask, request, render_template
import requests
import pandas as pd
import pickle
app = Flask(__name__)

# loading models
# movies = pd.read_csv('movies.csv')
movies = pickle.load(open('movies.pkl', 'rb'))
content_similarity = pickle.load(open('content_similarity.pkl', 'rb'))
user_movie_matrix = pickle.load(open('user_movie_matrix.pkl', 'rb'))
user_similarity_df = pickle.load(open('user_similarity.pkl', 'rb'))

# function to fetch movie poster
def fetch_poster(tmdb_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=390e76286265f7638bb6b19d86474639&language=en-US".format(int(tmdb_id))
    data = requests.get(url)
    data = data.json()
    full_path = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    return full_path

# function to get recommended movies
def get_recommendations(user_id, movie_title):
    # get the index of the selected movie
    movie_index = movies[movies['title'] == movie_title].index[0]
    # Get content-based similarity scores
    content_scores = list(enumerate(content_similarity[movie_index]))
    # Store content scores in dictionary
    content_score_dict = {}
    for i in content_scores:
        movie_name = movies.iloc[i[0]].title
        score = i[1]
        content_score_dict[movie_name] = score
    # Find similar users
    similar_users = user_similarity_df[user_id].sort_values(ascending=False)
    # Remove the selected user
    similar_users = similar_users.drop(user_id)
    # Get top 10 similar users
    top_users = similar_users.head(10)
    # Get movies already watched by selected user
    watched_movies = user_movie_matrix.loc[user_id].dropna().index
    # Store collaborative filtering scores
    collaborative_score_dict = {}
    # Loop through similar users
    for similar_user_id, similarity_score in top_users.items():
        # Get ratings from similar user
        similar_user_ratings = user_movie_matrix.loc[similar_user_id].dropna()
        # Loop through rated movies
        for movie_name, rating in similar_user_ratings.items():
            # Only recommend unseen movies
            if movie_name not in watched_movies:
                if movie_name not in collaborative_score_dict:
                    collaborative_score_dict[movie_name] = 0
                collaborative_score_dict[movie_name] += similarity_score * rating
    # Normalise collaborative scores
    max_collaborative_score = max(collaborative_score_dict.values())
    for movie_name in collaborative_score_dict:
        collaborative_score_dict[movie_name] = collaborative_score_dict[movie_name] / max_collaborative_score
    # Combine content and collaborative scores
    final_scores = {}
    for movie_name in collaborative_score_dict:
        content_score = content_score_dict.get(movie_name, 0)
        collaborative_score = collaborative_score_dict.get(movie_name, 0)
        final_score = (0.5 * content_score) + (0.5 * collaborative_score)
        final_scores[movie_name] = final_score
    # Sort final hybrid recommendations
    recommendations = sorted(
        final_scores.items(),
        key=lambda x: x[1],
        reverse=True)
    # Get top 20 movie names
    recommended_movie_titles = []
    for movie, score in recommendations[:20]:
        recommended_movie_titles.append(movie)
    # Get posters
    recommended_movie_posters = []
    for title in recommended_movie_titles:
        tmdb_id = movies[movies['title'] == title]['tmdbId'].values[0]
        recommended_movie_posters.append(fetch_poster(tmdb_id))
    return recommended_movie_titles, recommended_movie_posters

# home page
@app.route('/')
def home():
    movie_list = movies['title'].tolist()
    user_list = user_movie_matrix.index.tolist()
    return render_template('index.html', movie_list=movie_list, user_list=user_list)

# recommendation page
@app.route('/recommend', methods=['POST'])
def recommend():
    movie_title = request.form['selected_movie']
    user_id = int(request.form['selected_user'])
    recommended_movie_titles, recommended_movie_posters = get_recommendations(user_id, movie_title)
    return render_template('index.html', movie_list=movies['title'].tolist(),
                           recommended_movie_titles=recommended_movie_titles,
                           recommended_movie_posters=recommended_movie_posters)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)