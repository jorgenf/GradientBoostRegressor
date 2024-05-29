import data
import database
import server

FILE_PATH = "fangst.csv"
DISTRICT_ID = data.DISTRICTS.index("Vesterålen")
FISH_ID = data.FISH.index("Torsk")
TYPE_DESCRIPTION = "Antall kg fisket"

if __name__ == '__main__':

    session = database.connect()

    database.add_observed_data(session, FILE_PATH, TYPE_DESCRIPTION, FISH_ID, DISTRICT_ID)
    fishdata = session.query(database.Fish).all()
    print("Starting server")
    server.run_server()


