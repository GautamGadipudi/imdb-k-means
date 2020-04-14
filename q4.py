from sys import argv
from q2 import get_sample, insert_centroids, client as client1
from q3 import get_docs, assign_cluster_centers, update_cluster_centers, get_new_centroids, update_new_centroids, client as client2

import matplotlib.pyplot as plot

def get_command_line_args():
    k_min = k_max = k_step = iter_limit = 0
    if len(argv) == 5:
        k_min = int(argv[1])
        k_max = int(argv[2])
        k_step = int(argv[3])
        iter_limit = int(argv[4])
    elif len(argv) == 4:
        k_min = int(argv[1])
        k_max = int(argv[2])
        k_step = int(argv[3])
        iter_limit = int(input('Please enter a iteration limit: '))
    elif len(argv) == 3:
        k_min = int(argv[1])
        k_max = int(argv[2])
        k_step = int(input('Please enter a step for k value: '))
        iter_limit = int(input('Please enter a iteration limit: '))
    elif len(argv) == 2:
        k_min = int(argv[1])
        k_max = int(input('Please enter a stop value for k: '))
        k_step = int(input('Please enter a step for k value: '))
        iter_limit = int(input('Please enter a iteration limit: '))
    elif len(argv) == 1:
        k_min = int(input('Please enter a start value for k: '))
        k_max = int(input('Please enter a stop value for k: '))
        k_step = int(input('Please enter a step value for k: '))
        iter_limit = int(input('Please enter a iteration limit: '))
    return k_min, k_max, k_step, iter_limit


def get_SSE(clusters: list) -> float:
    SSE = 0
    for cluster in clusters:
        cluster_center = cluster['cluster_point']
        for point in cluster['points']:
            SSE += (cluster_center[0] - point[0]) ** 2
            SSE += (cluster_center[1] - point[1]) ** 2
    return SSE


def plot_graph(genre: str, k_SSE_dic: dict):
    plot.title(genre)
    k_list = []
    SSE_list = []
    for k in k_SSE_dic:
        k_list.append(k)
        SSE_list.append(k_SSE_dic[k])
    plot.plot(k_list, SSE_list)
    plot.savefig(f'{genre}_graph.jpg', format='jpeg')
    plot.clf()


if __name__ == "__main__":
    genres = ['Action', 'Horror', 'Romance', 'Sci-Fi', 'Thriller']
    k_min, k_max, k_step, iter_limit = get_command_line_args()
    for g in genres:
        print(f'******** Calculating for {g} ***********')
        docs = get_docs(g)
        k_SSE_dic = {}
        for k in range(k_min, k_max + 1, k_step):
            points = get_sample(k, g)
            isInserted, count = insert_centroids(points)
            clusters = []
            if isInserted:
                    print(f"Inserted {count} random docs into centroids collection.")
            for i in range(iter_limit):
                print(f'********** genre = {g} k = {k} iteration = {i + 1} ************')
                
                updated_docs = assign_cluster_centers(docs)
                match_count, update_count = update_cluster_centers(updated_docs)
                print(f'Updated {update_count} / {match_count} docs with new cluster.')
                clusters = get_new_centroids(g)
                match_count, update_count = update_new_centroids(clusters)
                print(f'Updated {update_count} / {match_count} docs with new centroid.')
                if update_count == 0:
                    break
                print('\n')
            SSE = get_SSE(clusters)
            k_SSE_dic[k] = SSE
        plot_graph(g, k_SSE_dic)
    client1.close()
    client2.close()
