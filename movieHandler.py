from imdb import IMDb


class Movie(object):
    def __init__(self, title):
        # create an instance of the IMDb class
        self.ia = IMDb()

        search_results = self.ia.search_movie(title)
        self.movie = None
        for movie in search_results:
            if movie["kind"] == "tv series" or movie["kind"] == "tv miniseries":
                self.movie = movie
                break

        # TV show check
        if movie["kind"] != "tv series" and movie["kind"] != "tv miniseries":
            self.movie = None
            print("That is not a tv series (kind = {})".format(movie["kind"]))
            return

        # Setting default vars
        self.ia.update(self.movie, 'main')  # takes between 1-2s

        self.id = self.movie.movieID
        self.kind = self.movie.get('kind')
        self.year = self.movie.get('year')
        self.title = self.movie.get('title')
        self.rating = self.movie.get('rating')

    def get_show_info(self):
        if self.kind == "tv series" or self.kind == "tv miniseries":
            self.ia.update(self.movie, 'episodes')

            returnData = {}
            seasons = self.movie['episodes']
            for season in sorted(seasons):
                returnData[season] = (len(seasons[season]))

            self.seasons = returnData

            return returnData


if __name__ == "__main__":
    movie = Movie("12 Monkeys 2015")
    r = movie.get_show_info()
    print(r)
