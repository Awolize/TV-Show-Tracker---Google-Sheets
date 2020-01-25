from movieHandler import Movie
import csv
import time
if __name__ == "__main__":
    shows = ['3%', '12 Monkeys 2015', '13 Reasons Why', '3Below: Tales of Arcadia', 'Agent Carter', 'Archer', 'Arrow', 'Black Lightning', 'Black Mirror', 'BoJack horseman', 'Breaking Bad', 'Brooklyn Nine-Nine', 'Cloak & Dagger', 'Continuum', 'Daredevil', "DC's Legends of Tomorrow", 'Designated Survivor', 'F is for Family', 'Falling skies', 'Fear The Walking Dead', 'Final Space', 'Friends', 'Game of Thrones', 'Gotham', 'how i met your mother', 'House of Cards', 'Iron Fist', 'Jessica Jones', 'Knightfall', 'La casa de papel', 'Limitless',
             'Lost in Space', 'Lucifer', 'Luke Cage', 'Misfits', 'Modern Family', 'Mr. robot', 'Narcos', 'Orphan Black', 'pine gap', 'Prison Break', 'Rick and Morty', 'Riverdale', 'Salvation', 'Scorpion', 'Sense8', 'Sherlock', 'Shooter', 'Silicon Valley', 'Spartacus', 'Stranger Things', 'Suits', 'SuperGirl 2015', 'The 100', 'The Blacklist', 'The Defenders', 'The end of the fucking world', 'The Expanse', 'The Flash', 'The Last Ship', 'The OA', 'The Punisher', 'The Walking Dead', 'Travelers', 'Trollhunter Tales of Arcadia', 'Van Helsing', 'Vikings', 'Westworld']

    if shows:
        start_time = time.time()
        everything = []
        for title in shows:
            movie = Movie(title)
            print("{} ({})".format(movie.title, movie.year))
            movie.get_show_info()
            everything.append([movie.title, len(movie.seasons)])
        print("--- %s seconds ---" % (time.time() - start_time))

    with open('everything.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(everything)
