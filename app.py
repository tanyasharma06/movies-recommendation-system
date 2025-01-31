import pickle
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', '')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Load data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html', movies=movies['title'].values)

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    movie_name = request.form['movie']
    recommended_movie_names, recommended_movie_posters = recommend(movie_name)
    return render_template('index.html', movies=movies['title'].values, 
                           recommended_movies=zip(recommended_movie_names, recommended_movie_posters))

if __name__ == '__main__':
    app.run(debug=True)
