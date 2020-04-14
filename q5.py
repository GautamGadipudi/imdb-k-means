import matplotlib.pyplot as plot
from pymongo import MongoClient
import numpy as np

from sys import argv
import random
from constants import CONNECTION_STRING, DATABASE_NAME, CLUSTER_COLLECTION_NAME, GENRE_K_DICT
from q2 import get_k_g, main as q2_main, client as client2
from q3 import main as q3_main, client as client3

client = MongoClient(CONNECTION_STRING)
db = client.get_database(DATABASE_NAME)


def get_clusters(g: str) -> list:
    return list(db.get_collection(CLUSTER_COLLECTION_NAME).aggregate([
    {
        '$match': {
            'genres': g
        }
    }, {
        '$group': {
            '_id': '$cluster', 
            'points': {
                '$push': '$kmeansNorm'
            }
        }
    }]))


def get_random_color(palette=[]):   
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    shapes = ['o', 's', 'p', 'd', 'D', '*', '+']
    color_index = random.randint(0, len(colors) - 1)
    shape_index = random.randint(0, len(shapes) - 1)
    result = f'{colors[color_index]}{shapes[shape_index]}'
    while result in palette:
        color_index = random.randint(0, len(colors) - 1)
        shape_index = random.randint(0, len(shapes) - 1)
        result = f'{colors[color_index]}{shapes[shape_index]}'
    return result

def plot_points(clusters: list, g: str):
    plot.title(g)
    plot.xlabel('Normalized startYear')
    plot.ylabel('Normalized avgRating')
    plot.xticks(np.arange(0, 1.2, 0.1))
    plot.yticks(np.arange(0, 1.2, 0.1))
    for cluster in clusters:
        cluster_colors = []
        cluster_color = get_random_color(cluster_colors)
        cluster_colors.append(cluster_color)
        for point in cluster['points']:
            plot.plot(point[0], point[1], cluster_color, markersize=5)
    
    plot.savefig(f'./img/q5/{g}.jpg', format='jpg')
    plot.clf()


def main():
    if len(argv) == 1:
        for g in GENRE_K_DICT:
            q2_main(GENRE_K_DICT[g], g)
            q3_main(g)
            clusters = get_clusters(g)
            plot_points(clusters, g)
    else:
        k, g = get_k_g()
        q2_main(k, g)
        q3_main(g)
        clusters = get_clusters(g)
        plot_points(clusters, g)
    client2.close()
    client3.close()

if __name__ == "__main__":
    main()




