from sys import argv
from q2 import get_sample, insert_centroids
from q3 import get_docs, assign_cluster_centers, update_cluster_centers, get_new_centroids, update_new_centroids

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

if __name__ == "__main__":
    genres = ['Comedy']
    k_min, k_max, k_step, iter_limit = get_command_line_args()
    for g in genres:
        docs = get_docs(g)
        k_SSE_dic = {}
        for k in range(k_min, k_max + 1, k_step):
            points = get_sample(k, g)
            isInserted, count = insert_centroids(points)
            clusters = []
            if isInserted:
                    print(f"Inserted {count} random docs into centroids collection.")
            for i in range(iter_limit):
                print(f'********** k = {k} iteration = {i + 1} ************')
                
                updated_docs = assign_cluster_centers(docs)
                match_count, update_count = update_cluster_centers(updated_docs)
                print(f'Updated {update_count} / {match_count} docs with new cluster.')
                clusters = get_new_centroids(g)
                match_count, update_count = update_new_centroids(clusters)
                print(f'Updated {update_count} / {match_count} docs with new centroid.')
                print('\n')
            sse = get_SSE(clusters)
            k_SSE_dic[k] = sse
        plot(g, k_SSE_dic)
