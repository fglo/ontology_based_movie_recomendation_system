from fastapi import APIRouter
import collections
from .. import onto

onto = onto.get()

router = APIRouter()

@router.get("/owl/movies", tags=["movies"])
async def get_all_movies():
    global onto
    return [ind.name for ind in list(onto.get_instances_of(onto["Film"]))]

@router.get("/owl/movies/liked", tags=["movies"])
async def get_most_liked_movies():
    global onto
    movies = {}
    for user in list(onto.get_instances_of(onto["Uzytkownik"])):
        for movie in list(user.Uzytkownik_lubi_Film):
            if movie.name not in movies:
                movies[movie.name] = 0
            movies[movie.name] += 1

    mean = 0
    for key, val in  movies.items():
        mean += val
    mean /= len(movies.keys())

    most_liked = []
    for key, val in  movies.items():
        if val >= mean:
            most_liked.append(key)

    sorted(most_liked, reverse=True)
    return most_liked

@router.get("/owl/movies/watched", tags=["movies"])
async def get_most_watched_movies():
    global onto
    movies = {}
    for user in list(onto.get_instances_of(onto["Uzytkownik"])):
        for movie in list(user.Uzytkownik_ogladal_Film):
            if movie.name not in movies:
                movies[movie.name] = 0
            movies[movie.name] += 1

    mean = 0
    for key, val in  movies.items():
        mean += val
    mean /= len(movies.keys())

    most_watched = []
    for key, val in  movies.items():
        if val >= mean:
            most_watched.append(key)

    sorted(most_watched, reverse=True)
    return most_watched
    
@router.get("/owl/movies/categories/liked", tags=["movies"])
async def get_most_liked_movies_by_category():
    global onto
    categories = {}
    for cat in list(onto.get_instances_of(onto["Kategoria"])):
        categories[cat.name] = {}
        for movie in list(cat.Kategoria_przypisana_do_Film):
            for user in list(movie.Film_jest_polubiony_przez_Uzytkownik):
                if movie.name not in categories[cat.name]:
                    categories[cat.name][movie.name] = 0
                categories[cat.name][movie.name] += 1
            categories[cat.name] = dict(sorted(categories[cat.name].items(), key=lambda item: item[1], reverse=True))
            
    return categories

@router.get("/owl/movies/categories/watched", tags=["movies"])
async def get_most_watched_movies_by_category():
    global onto
    categories = {}
    for cat in list(onto.get_instances_of(onto["Kategoria"])):
        categories[cat.name] = {}
        for movie in list(cat.Kategoria_przypisana_do_Film):
            for user in list(movie.Film_byl_ogladany_przez_Uzytkownik):
                if movie.name not in categories[cat.name]:
                    categories[cat.name][movie.name] = 0
                categories[cat.name][movie.name] += 1
            categories[cat.name] = dict(sorted(categories[cat.name].items(), key=lambda item: item[1], reverse=True))
            
    return categories

@router.get("/owl/movies/categories/{category}", tags=["movies"])
async def get_movies_of_category(category : str):
    global onto
    movies = []
    for cat in list(onto.get_instances_of(onto["Kategoria"])):
        if cat.name == category:
            movies =  [ind.name for ind in list(cat.Kategoria_przypisana_do_Film)]
            break
    return movies

@router.get("/owl/movies/series/{seriesname}", tags=["movies"])
async def get_movies_of_series(seriesname : str):
    global onto
    movies = []
    for series in list(onto.get_instances_of(onto["Seria"])):
        if series.name == seriesname:
            movies = [ind.name for ind in list(series.Seria_zawiera_Film)]
            break
    return movies
    
@router.get("/owl/movies/users/liked/{username}", tags=["movies"])
async def get_users_liked_movies(username : str):
    global onto
    movies = []
    for user in list(onto.get_instances_of(onto["Uzytkownik"])):
        if user.name == username:
            for movie in list(user.Uzytkownik_lubi_Film):
                movies.append({
                    'movie': movie.name,
                    'categories': [cat.name for cat in list(movie.Film_jest_Kategoria)]
                })
    return movies

@router.get("/owl/movies/users/watched/{username}", tags=["movies"])
async def get_users_watched_movies(username : str):
    global onto
    movies = []
    for user in list(onto.get_instances_of(onto["Uzytkownik"])):
        if user.name == username:
            for movie in list(user.Uzytkownik_ogladal_Film):
                movies.append({
                    'movie': movie.name,
                    'categories': [cat.name for cat in list(movie.Film_jest_Kategoria)]
                })
    return movies

@router.get("/owl/movies/similar/users/{username}", tags=["movies"])
async def get_recommended_watched_movies_from_similar_users(username : str):
    global onto
    movies = []
    for user in list(onto.get_instances_of(onto["Uzytkownik"])):
        if user.name == username:
            movies = list(user.Uzytkownik_ogladal_Film)

    users = {}
    for movie in movies:
        for user in list(movie.Film_byl_ogladany_przez_Uzytkownik):
            if user.name != username:
                if user.name not in users:
                    users[user.name] = { 'user': user, 'similar_movies_count': 0 }
                users[user.name]['similar_movies_count'] += 1
    
    recommended_movies = []
    for user in users.values():
        # recommended_movies.append({'name': user['user'].name, 'percent': user['similar_movies_count'] / len(movies)})
        if user['similar_movies_count'] / len(movies) >= 0.7:
            for movie in list(user['user'].Uzytkownik_ogladal_Film):
                if movie not in movies and movie.name not in recommended_movies:
                    recommended_movies.append(movie.name)

    return recommended_movies

@router.get("/owl/movies/similar/parameters/{username}", tags=["movies"])
async def get_recommended_similar_movies(username : str):
    global onto
    movies = []
    for user in list(onto.get_instances_of(onto["Uzytkownik"])):
        if user.name == username:
            movies = list(user.Uzytkownik_ogladal_Film)

    actors = {}
    for movie in movies:
        for actor in list(movie.Film_obsadza_Aktor):
            if actor.name not in actors:
                actors[actor.name] = { 'actor': actor, 'similar_movies_count': 0 }
            actors[actor.name]['similar_movies_count'] += 1
    
    tags = {}
    for movie in movies:
        for tag in list(movie.Film_posiada_Tag):
            if tag.name not in tags:
                tags[actor.name] = { 'tag': tag, 'similar_movies_count': 0 }
            tags[actor.name]['similar_movies_count'] += 1
            
    categories = {}
    for movie in movies:
        for category in list(movie.Film_jest_Kategoria):
            if category.name not in categories:
                categories[category.name] = { 'category': category, 'similar_movies_count': 0 }
            categories[category.name]['similar_movies_count'] += 1

    recommended_movies = []
    for actor in actors.values():
        if actor['similar_movies_count'] >= 1:
            for movie in list(actor['actor'].Aktor_gra_w_Film):
                if movie not in movies and movie.name not in recommended_movies:
                    recommended_movies.append(movie.name)
    for tag in tags.values():
        if tag['similar_movies_count'] >= 1:
            for movie in list(tag['tag'].Tag_przypisany_do_Film):
                if movie not in movies and movie.name not in recommended_movies:
                    recommended_movies.append(movie.name)
    for category in categories.values():
        if category['similar_movies_count'] >= 1:
            for movie in list(category['category'].Kategoria_przypisana_do_Film):
                if movie not in movies and movie.name not in recommended_movies:
                    recommended_movies.append(movie.name)

    return recommended_movies

@router.get("/owl/movies/similar/series/{username}", tags=["movies"])
async def get_recommended_similar_series(username : str):
    global onto
    movies = []
    for user in list(onto.get_instances_of(onto["Uzytkownik"])):
        if user.name == username:
            movies = list(user.Uzytkownik_ogladal_Film)

    recommended_movies = []
    for movie in movies:
        for series in list(movie.Film_jest_z_Seria):
            for movie2 in list(series.Seria_zawiera_Film):
                if movie2 not in movies and movie2.name not in recommended_movies:
                    recommended_movies.append(movie2.name)

    return recommended_movies

@router.get("/owl/movies/recommended/{username}", tags=["movies"])
async def get_recommended_movies(username : str):
    global onto
    recommended_movies = {
        "others_watched": [],
        "similar_movies": [],
        "rest_from_series": []
    }
    for movie in await get_recommended_watched_movies_from_similar_users(username):
        if movie not in recommended_movies["others_watched"]:
            recommended_movies["others_watched"].append(movie)
    for movie in await get_recommended_similar_movies(username):
        if movie not in recommended_movies["similar_movies"]:
            recommended_movies["similar_movies"].append(movie)
    for movie in await get_recommended_similar_series(username):
        if movie not in recommended_movies["rest_from_series"]:
            recommended_movies["rest_from_series"].append(movie)

    return recommended_movies

@router.get("/owl/movies/watch/{username}/{moviename}", tags=["movies"])
async def watch_movie(username : str, moviename : str):
    global onto
    user = None
    for user in list(onto.get_instances_of(onto["Uzytkownik"])):
        if user.name == username:
            break
    
    movie = None
    for movie in list(onto.get_instances_of(onto["Film"])):
        if movie.name == moviename:
            break
    
    if user is not None and movie is not None:
        user.Uzytkownik_ogladal_Film.append(movie)
        sync_reasoner(onto, infer_property_values = True)


@router.get("/owl/movies/like/{username}/{moviename}", tags=["movies"])
async def watch_movie(username : str, moviename : str):
    global onto
    user = None
    for user in list(onto.get_instances_of(onto["Uzytkownik"])):
        if user.name == username:
            break
    
    movie = None
    for movie in list(onto.get_instances_of(onto["Film"])):
        if movie.name == moviename:
            break
    
    if user is not None and movie is not None:
        user.Uzytkownik_lubi_Film.append(movie)
        sync_reasoner(onto, infer_property_values = True)