import pickle
import os.path

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from movieHandler import Movie
from spreadsheetHandler import Spreadsheet

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def login():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'config/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    return service


def get_movie_from_user():
    title = ""
    while 1:
        title = input('Title of the tv show: ')
        movie = Movie(title)
        print("")

        if movie.kind == "tv series" or movie.kind == "tv miniseries":
            print("{}: {}".format(movie.title, movie.year))
            confirmation = input(
                "is this the correct tv show? (y/n): ")
            print("")
            if confirmation == "y":
                return movie
        else:
            print("Could not find tv show.")
        break

    return None

def menu(sp):
    menu = '''[1] Add new tv show\n[2] Remove all sheets (but ToC)\n[3] Update IMDB rating\n[4] Exit\n'''
    while 1:
        print(menu)
        choice = input('Menu option: ')
        if choice == "1":
            movie = get_movie_from_user()
            if movie:
                print("Getting tv series information...")
                movie.get_show_info()
                print("Setting up page...")
                sp.create_page(movie)
        elif choice == "2":
            print("Removing sheets...")
            sp.remove_all()
        elif choice == "3":
            print("Updating IMDB rating...")
            # get title list (tv shows) [A2:A]
            titles = sp.get_all_titles()

            # Call boye to import imdb score
            column_index = sp.find_header("ToC", text="IMDB")

            for row_index, title in enumerate(titles):
                movie = Movie(title)
                #update spreadsheet (title, rating)
                sp.update_rating("ToC", column_index, row_index, movie.rating)

        elif choice == "4":
            print("Bye bye!")
            break
        else:
            print("Input is not an options.")

        print("Done.\n")

if __name__ == '__main__':
    service = login()  # create token
    sp = Spreadsheet(service)

    shows = ['3%', '12 Monkeys 2015', '13 Reasons Why', '3Below: Tales of Arcadia', 'Agent Carter', 'Archer', 'Arrow', 'Black Lightning', 'Black Mirror', 'BoJack horseman', 'Breaking Bad', 'Brooklyn Nine-Nine', 'Cloak & Dagger', 'Continuum', 'Daredevil', "DC's Legends of Tomorrow", 'Designated Survivor', 'F is for Family', 'Falling skies', 'Fear The Walking Dead', 'Final Space', 'Final Space', 'Friends', 'Game of Thrones', 'Gotham', 'how i met your mother', 'House of Cards', 'Iron Fist', 'Jessica Jones', 'Knightfall', 'La casa de papel', 'Limitless', 'Lost in Space',
             'Lucifer', 'Luke Cage', 'Misfits', 'Modern Family', 'Mr. robot', 'Narcos', 'Orphan Black', 'pine gap', 'Prison Break', 'Rick and Morty', 'Riverdale', 'Riverdale', 'Salvation', 'Scorpion', 'Sense8', 'Sherlock', 'Shooter', 'Silicon Valley', 'Spartacus', 'Stranger Things', 'Suits', 'SuperGirl 2015', 'The 100', 'The Blacklist', 'The Defenders', 'The end of the fucking world', 'The Expanse', 'The Flash', 'The Last Ship', 'The OA', 'The Punisher', 'The Walking Dead', 'Travelers', 'Trollhunter Tales of Arcadia', 'Van Helsing', 'Vikings', 'Westworld']

    shows = []
    if shows:
        for title in shows:
            movie = Movie(title)
            print("{} ({})".format(movie.title, movie.year))
            movie.get_show_info()
            sp.create_page(movie)
    else:
        menu(sp)
