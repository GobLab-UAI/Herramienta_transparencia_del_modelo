from pymongo import MongoClient
import uuid

# Información de conexión a MongoDB
MONGO_URI = "mongodb+srv://goblab:acCH0G67KtgmmN1y@goblab.eih8e7t.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "model_cards"
COLLECTION_NAME = "runs"

client = MongoClient(MONGO_URI)
