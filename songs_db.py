import sqlite3


class songs():

    con = sqlite3.connect('song_DB.db')

    cur = con.cursor()

    def __init__(self):
        self.cur.execute("""CREATE TABLE songs(
            song_name text
             )
            """)

    def add_song(self, name):
        self.cur.execute("INSERT INTO songs VALUES(name)")
