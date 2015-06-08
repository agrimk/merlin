import click
import tmdbsimple as tmdb
import time

tmdb.API_KEY = 'deb5d2f55e284931baf4f7e7020cfe44'
a = tmdb.API_KEY

genreDict = {u'Action': 28,
 u'Adventure': 12,
 u'Animation': 16,
 u'Comedy': 35,
 u'Crime': 80,
 u'Documentary': 99,
 u'Drama': 18,
 u'Family': 10751,
 u'Fantasy': 14,
 u'Foreign': 10769,
 u'History': 36,
 u'Horror': 27,
 u'Music': 10402,
 u'Mystery': 9648,
 u'Romance': 10749,
 u'Science Fiction': 878,
 u'TV Movie': 10770,
 u'Thriller': 53,
 u'War': 10752,
 u'Western': 37}

numToGenre = {1: u'Action',
 2: u'Adventure',
 3: u'Animation',
 4: u'Comedy',
 5: u'Crime',
 6: u'Documentary',
 7: u'Drama',
 8: u'Family',
 9: u'Fantasy',
 10: u'Foreign',
 11: u'History',
 12: u'Horror',
 13: u'Music',
 14: u'Mystery',
 15: u'Romance',
 16: u'Science Fiction',
 17: u'TV Movie',
 18: u'Thriller',
 19: u'War',
 20: u'Western'}

# Movie class

class Movie:

    def __init__(self,title,ID,lan,genres,overview,rating):
        self.title = title
        self.ID = ID
        self.lan = lan
        self.genres = genres
        self.overview = overview
        self.rating = rating

    def get_title(self):
        return self.title

    def get_id(self):
        return self.ID

    def get_lan(self):
        return self.lan

    def get_genres(self):
        return self.genres

    def get_overview(self):
        return self.overview

    def get_rating(self):
        return self.rating 
    
    def __repr__(self):
        return self.title

# Helper Function

def findPerson(name):
    search = tmdb.Search()
    nID = {}
    tries = 0
    while tries < 4:
        tries += 1
        try:    
            response = search.person(query=name)
            for i in xrange(3):
                nID[(i + 1,response['results'][i]['name'])] = response['results'][i]['id'] 
            break
        except:
            continue
    return nID

def discoverMovie(genre,people):

    discover = tmdb.Discover()
    tries = 0
    response = None
    while tries < 4:
        tries += 1
        try:
            response = discover.movie(with_people=people,with_genres=genre)
            break
        except:
            continue 
    r = None
    if response:    
        r = response['results']
    result = {}

    if response:
        for i in xrange(len(r)):
            m = Movie(r[i]['title'],r[i]['id'],r[i]['original_language'],r[i]['genre_ids'],r[i]['overview'],r[i]['vote_average'])
            result[i + 1] = m

    return result 

@click.command()
def discover():
    click.echo("Let's find you a Movie\n")
    for i in xrange(10):
        print '.',
        time.sleep(0.1)
    print '\n' 
    # Get the Genre
    for key in sorted(numToGenre.iterkeys()):
        click.echo(str(key) + '. ' + numToGenre[key].encode('ascii','ignore'))
    genre = click.prompt('Pick a Genre(comma separated) ')
    gList = genre.split(',')
    genre = ''
    for i in xrange(len(gList)):
        genre += str(genreDict[numToGenre[int(gList[i])]])
        genre += ','
    genre = genre[:-1]

    # Get the Cast
    click.echo('Pick the cast and crew, Be as specific as you can and avoid spelling mistakes\n')
    people = ''
    while True:
        search = tmdb.Search()
        name = click.prompt('Give me a name')

        result = findPerson(name)
        if (result):
            for key in sorted(result.iterkeys()):
                add = click.confirm('Are you looking for ' + key[1].encode('ascii','ignore'))
                if add:
                    people += str(result[key])
                    people += ','
                    break;
        else:
            print 'Sorry, try again'
         
        confirm = click.confirm('You want to add more people')
        if (confirm == False):
            break
    people = people[:-1]

    # Get results
    click.echo('Sit back and Relax\n')
    movies = discoverMovie(genre,people)
    if movies:
        for key in sorted(movies.iterkeys()):
            print movies[key].get_title(),
            print movies[key].get_rating()
            print movies[key].get_overview()
            print '\n'
