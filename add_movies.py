# save_items.py

import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moviesstore.settings')
django.setup()

from movies.models import Movie
import requests
import json

'''
Gets all movies from page 1-num_pages, writes the poster to proper directory, 
and returns info needed to create a movie and add to database
'''
def get_movies(num_pages):
    for page in range(1, num_pages):
        url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=" + str(page) + "&sort_by=popularity.desc"
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwZjUxMTkyN2RiYWEwYjU4ZTkzNmI1ZjZjMDFmNWQ1MyIsIm5iZiI6MTczOTQ4MDAwMi43MzcsInN1YiI6IjY3YWU1YmMyZjI4ZDk1YWRiM2QwZDZkOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.MpgP6sQF1m0kXBLBeNEzfDKsEGlOP4Ew3PRcrOSQ4QU"
        }
        response = requests.get(url, headers=headers)
        movies = json.loads(response.text)['results']
        for movie in movies:
            title = movie['original_title']
            desc = movie['overview']
            img_url = 'https://image.tmdb.org/t/p/original/' + movie['poster_path']
            img_path = 'media/movie_images/' + title.replace(' ', '_') + '.jpg'
            img_data = requests.get(img_url).content
            with open(img_path, 'wb') as handler:
                handler.write(img_data)
            Movie.objects.create(name=title, price=5, description=desc, image=img_path[img_path.index('/movie_images'):])

def rename_movies():
    movies = Movie.objects.all()
    for movie in movies:
        path = 'media/' + str(movie.image).strip('/')
        new_path = 'media/movie_images/' + str(movie.id) + '.jpg'
        try:
            os.rename(path, new_path)
        except FileNotFoundError:
            movie.delete()
            continue
        movie.image = new_path[new_path.index('/movie_images'):]
        movie.save()

rename_movies()