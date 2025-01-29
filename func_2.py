movies = [
    {"name": "Usual Suspects", "imdb": 7.0, "category": "Thriller"},
    {"name": "Hitman", "imdb": 6.3, "category": "Action"},
    {"name": "Dark Knight", "imdb": 9.0, "category": "Adventure"},
    {"name": "The Help", "imdb": 8.0, "category": "Drama"},
    {"name": "The Choice", "imdb": 6.2, "category": "Romance"},
    {"name": "Colonia", "imdb": 7.4, "category": "Romance"},
    {"name": "Love", "imdb": 6.0, "category": "Romance"},
    {"name": "Bride Wars", "imdb": 5.4, "category": "Romance"},
    {"name": "AlphaJet", "imdb": 3.2, "category": "War"},
    {"name": "Ringing Crime", "imdb": 4.0, "category": "Crime"},
    {"name": "Joking muck", "imdb": 7.2, "category": "Comedy"},
    {"name": "What is the name", "imdb": 9.2, "category": "Suspense"},
    {"name": "Detective", "imdb": 7.0, "category": "Suspense"},
    {"name": "Exam", "imdb": 4.2, "category": "Thriller"},
    {"name": "We Two", "imdb": 7.2, "category": "Romance"}
]

def is_highly_rated(movie_name):
    for movie in movies:
        if(movie["name"] == movie_name):
            print(movie["imdb"] > 5.5)
    print("\n")

def get_highly_rated_movies(movies):
    for movie in movies:
        if(movie["imdb"] > 5.5):
            print(movie["name"])
        
    print("\n")

def get_movies_by_category(movie_list, category):
    for movie in movies:
        if(movie["category"] == category):
            print(movie["name"])
    print("\n")
    
def get_average_score(movie_list):
    sum = 0
    num = 0
    for movie in movies:
        sum += movie["imdb"]
        num+=1
    print(sum/num)
    print("\n")

def get_average_score_by_category(movie_list, category):
    l = []
    sum = 0
    for movie in movies:
        if(movie["category"] == category):
            l.append(movie["name"])
            sum+=movie["imdb"]
    print(sum/len(l))
    print("\n")
is_highly_rated("Usual Suspects")
get_highly_rated_movies(movies)
get_movies_by_category(movies,"Thriller")
get_average_score(movies)
get_average_score_by_category(movies,"Thriller")
