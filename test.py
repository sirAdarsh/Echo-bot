import sqlite3

# temporary memory data :: conn = sqlite3.connect(':connect:')

conn = sqlite3.connect('customer.db')

#Create a cursor
myCur = conn.cursor()

# insert a data
myCur.execute("INSERT INTO customers VALUES('Adarsh', 'Sinha', 'aksinha.dhn@gmail.com')")

#commit our command
conn.commit()

#close our connection
conn.close()
