import warnings
warnings.filterwarnings("ignore")

from sys import argv
from scipy.spatial import distance
from pymongo import MongoClient

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


def assign_cluster_centers(docs: list) -> list:
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


def update_cluster_centers(docs: list) -> (int, int):
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


def get_new_centroids(g: str) -> list:
    points_grouped_by_centroid = list(db.get_collection('moviesToCluster').aggregate([
        {
            '$match': {
                'genres': g
            }
        }, {
            '$lookup': {
                'from': 'centroids', 
                'localField': 'cluster', 
                'foreignField': 'point', 
                'as': 'cluster_object'
            }
        }, {
            '$addFields': {
                'cluster_id': {
                    '$arrayElemAt': [
                        '$cluster_object._id', 0
                    ]
                }, 
                'cluster_point': {
                    '$arrayElemAt': [
                        '$cluster_object.point', 0
                    ]
                }
            }
        }, {
            '$group': {
                '_id': {
                    'cluster_id': '$cluster_id', 
                    'cluster_point': '$cluster_point'
                }, 
                'points': {
                    '$push': '$kmeansNorm'
                }
            }
        }, {
            '$addFields': {
                '_id': '$_id.cluster_id', 
                'cluster_point': '$_id.cluster_point'
            }
        }
    ]))
    
    new_centroids = []
    for centroid in points_grouped_by_centroid:
        points = centroid['points']
        n = len(points)
        new_centroid_point = [0, 0]
        new_centroid = {'_id': centroid['_id']}
        for point in points:
            new_centroid_point[0] += point[0]
            new_centroid_point[1] += point[1]
        new_centroid_point[0] /= n
        new_centroid_point[1] /= n
        new_centroid['point'] = new_centroid_point
        new_centroids.append(new_centroid)

    return new_centroids

    
def update_new_centroids(new_centroids: list) -> ():
    bulk = db.get_collection('centroids').initialize_unordered_bulk_op(True)
    for centroid in new_centroids:
        bulk.find({
            '_id': centroid['_id']
        }).update({
            '$set': {
                'point': centroid['point']
            }
        })
    x = bulk.execute()
    return x['nMatched'], x['nModified']

if __name__ == "__main__":
    g = get_g()
    docs = get_docs(g)
    updated_docs = assign_cluster_centers(docs)
    match_count, update_count = update_cluster_centers(updated_docs)
    print(f'Updated {update_count} / {match_count} docs with new cluster.')
    new_centroids = get_new_centroids(g)
    match_count, update_count = update_new_centroids(new_centroids)
    print(f'Updated {update_count} / {match_count} docs with new centroid.')
    