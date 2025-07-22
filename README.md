# Clustering movies from IMDB dataset

## Finding the best k (cluster size) for each genre
We follow the [elbow-method](https://www.geeksforgeeks.org/machine-learning/elbow-method-for-optimal-value-of-k-in-kmeans/) to find an optimal cluster size for each genre.

In the root of the repo, run the following:
```bash
python3 q4.py 10 50 5 100
```
The args are `k_min`, `k_max`, `k_step`, `iter_limit` respectively.

You can see the graphs in `./img/q4` directory. Below are the graphs of one particular test.

> **Action**: 
>
> ![Action genre graph](./img/static/q4/Action.jpg)
> 
> k = 25

> **Romance**: 
>
> ![Romance genre graph](./img/static/q4/Romance.jpg)
> 
> k = 35

> **Horror**: 
>
> ![Horror genre graph](./img/static/q4/Horror.jpg)
>
> k = 20

> **Sci-Fi**: 
>
> ![Sci-Fi genre graph](./img/static/q4/Sci-Fi.jpg)
> 
> k = 20

> **Thriller**: 
>
> ![Thriller genre graph](./img/static/q4/Thriller.jpg)
>
> 15

## Resulting clusters for subset of the dataset
In the root of the repo, run the following:
```bash
python3 q5.py
```
You can see the graphs in `./img/q5` directory. Below are the graphs of one particular test.
> **Action Clusters**: 
>
> ![Action genre clusters](img/static/q5/Action.jpg)
> 
> Consider the cluster of red plus(<span style="color:red">+</span>). It shows the action movies released in the normalized startYear of 0.35 to 0.55 (equivalent to approximately 1951 to 1971) are all rated between 6.5 and 9.1.

> **Thriller Clusters**: 
>
> ![Thriller genre clusters](img/static/q5/Thriller.jpg)
>
> Consider the cluster of black stars (<span style="color:black">★</span>). It shows that these thriller movies which are released between the years 1976 to 2018 are all not that great (have a rating of 4/10 or lower).

> **Romance Clusters**: 
>
> ![Romance genre clusters](img/static/q5/Romance.jpg)
> 
> Consider the cluster of black pentagons (<span style="color:black">⬟</span>). It shows all the latest movies (released in the past decade) of genre "Romance" that are very good (rated between 8 and 9).

> **Horror Clusters**: 
>
> ![Horror genre clusters](img/static/q5/Horror.jpg)
>
> Consider the cluster of green circles (<span style="color:green">●</span>, not <span style="color:green">◆</span>). It shows all the moderately rated (5.5 to 7) horror movies between the years 1996 and 2007.

> **Sci-Fi Clusters**: 
>
> ![Sci-Fi genre clusters](img/static/q5/Sci-Fi.jpg)
>
> Consider the cluster of black stars (<span style="color:black">★</span>). It shows the moderately rated Sci-Fi movies released between the years 1976 and 1996.

