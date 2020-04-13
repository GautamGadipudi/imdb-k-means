
from scipy.spatial import distance
from pymongo import MongoClient
from sys import argv

client = MongoClient('mongodb://localhost:27017/')
db = client.imdb


def get_g() -> str:
    genre = ''
    if len(argv) == 2:
        genre = argv[1]
    elif len(argv) == 1:
        genre = input('Please enter a genre: ')
    return genre


def get_docs(g: str) -> list:
    movies_cursor = db.get_collection('moviesToCluster').find({
        'genres': {
            '$exists': True,
            '$eq': g
        } 
    },
    {
        'genres': 1, 'kmeansNorm': 1
    })
    docs = list(movies_cursor)
    return docs


def get_centroids() -> list:
    centroids_cursor = db.get_collection('centroids').find({})
    return list(doc['point'] for doc in centroids_cursor)


def assign_cluster_center(docs: list):
    centroids = get_centroids()
    for doc in docs:
        point = doc['kmeansNorm']
        closest_centroid = [float('inf'), float('inf')]
        closest_distance = float('inf')
        for centroid in centroids:
            dist = distance.euclidean(centroid, point)
            if dist < closest_distance:
                closest_distance = dist
                closest_centroid = centroid
        doc['cluster'] = closest_centroid
    return docs  


def update_cluster_center(docs: list):
    bulk = db.get_collection('moviesToCluster').initialize_unordered_bulk_op(True)
    for doc in docs:
        bulk.find({
                '_id': doc['_id']
            }).update({
                '$set': {
                    'cluster': doc['cluster']
                }
            })
    x = bulk.execute()
    return x['nMatched'], x['nModified']


if __name__ == "__main__":
    g = get_g()
    docs = get_docs(g)
    updated_docs = assign_cluster_center(docs)
    match_count, update_count = update_cluster_center(updated_docs)
    print(f'Updated {update_count} / {match_countCo} docs in moviesToCluster')
    