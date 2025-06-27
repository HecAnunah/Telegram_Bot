from database.peewe_model import db, Client

base = db.connect()
clients = Client.select()

for cl in clients:
    print(cl)
