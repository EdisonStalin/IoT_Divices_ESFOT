from pymongo import MongoClient ## conexión a la base de datos

## Información del client de la base de datos.
client= 'edison'
passdb = 'GnzNw2aAyJjKGOs7'
dbname = 'iotecuador'

## Conexión MongoAtlas
def get_db():
    try:
        url_client = MongoClient("mongodb+srv://edison:GnzNw2aAyJjKGOs7@iotecuador.qbeh8.mongodb.net/iotecuador?retryWrites=true&w=majority")
        mydb = url_client.iotecuador
    except ConnectionError:
        print ("Error de coneccion con el servidor: --->"+client)
    return mydb



db.collection.updateMany(
  {},
  [{ "$set": { "dateField": { "$toDate": "$dateField" } }]
);