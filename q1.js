db = connect('localhost:27017/imdb');

db.moviesToCluster.drop();

db.movies.aggregate([{
    $match: {
        startYear: {
            $exists: true
        },
        avgRating: {
            $exists: true
        },
        type: "movie",
        numVotes: {
            $gt: 10000
        }
    }
}, {
    $group: {
        _id: null,
        maxAvgRating: {
            $max: "$avgRating"
        },
        minAvgRating: {
            $min: "$avgRating"
        },
        maxStartYear: {
            $max: "$startYear"
        },
        minStartYear: {
            $min: "$startYear"
        },
        data: {
            $push: "$$ROOT"
        }
    }
}, {
    $unwind: {
        path: "$data"
    }
}, {
    $addFields: {
        "data.kmeansNorm": [{
            $divide: [{
                $subtract: ["$data.startYear", "$minStartYear"]
            },
            {
                $subtract: ["$maxStartYear", "$minStartYear"]
            }
            ]
        },
        {
            $divide: [{
                $subtract: ["$data.avgRating", "$minAvgRating"]
            },
            {
                $subtract: ["$maxAvgRating", "$minAvgRating"]
            }
            ]
        }
        ]
    }
}, {
    $replaceRoot: {
        newRoot: "$data"
    }
}, {
    $out: 'moviesToCluster'
}]);

print('*** Dumped data into collection moviesToCluster collection! ***');

