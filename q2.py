from pymongo import MongoClient
from sys import argv

from constants import CONNECTION_STRING, DATABASE_NAME, CLUSTER_COLLECTION_NAME, CENTROIDS_COLLECTION_NAME

client = MongoClient(CONNECTION_STRING)
db = client.get_database(DATABASE_NAME)


def get_k_g() -> (int, str):
    k = 0
    genre = ''
    if len(argv) == 3:
        k = int(argv[1])
        genre = argv[2]
    elif len(argv) == 2:
        k = int(argv[1])
        genre = input('Please enter a genre: ')
    elif len(argv) == 1:
        k = int(input('Please enter a value for k: '))
        genre = input('Please enter a genre: ')
    return k, genre


def get_sample(k: int, g: str) -> list:
    result = []
    
    data = db.get_collection(CLUSTER_COLLECTION_NAME).aggregate([
        {
            '$match': {
                'genres': g
            }
        }, {
            '$sample': {
                'size': k
            }
        }, {
            '$project': {
                '_id': 0, 
                'kmeansNorm': 1
            }
        }
    ])
    for doc in data:
        result.append(doc['kmeansNorm'])
    return result


def insert_centroids(points: list):
    docs = []
    _id = 1
    for point in points:
        doc = {}
        doc['_id'] = _id
        doc['point'] = point
        docs.append(doc)
        _id += 1
    db.drop_collection(CENTROIDS_COLLECTION_NAME)
    x = db.get_collection(CENTROIDS_COLLECTION_NAME).insert_many(docs)
    return x.acknowledged, len(x.inserted_ids)


if __name__ == "__main__":
    k, g = get_k_g()
    points = get_sample(k, g)
    isInserted, count = insert_centroids(points)
    if isInserted:
        print(f"Inserted {count} docs into {CENTROIDS_COLLECTION_NAME} collection.")
    client.close()