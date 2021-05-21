import numpy as np
from scipy.spatial.distance import cdist

class ThingVectorizer:
    def __init__(self, delimiter=',', max_things=None):
        self.delimiter = delimiter
        if max_things:
            self.max_things = max_things
        else:
            self.max_things = np.inf

    def __repr__(self):
        return f'ThingVectorizer(delimiter="{self.delimiter}", max_things={self.max_things})'

    def fit(self, X):
        self.things = []
        for row in X:
            for thing in row.split(self.delimiter):
                if (thing not in self.things) and (len(self.things) < self.max_things):
                    self.things.append(thing)
        return self

    def transform(self, X):
        Xt = np.zeros((len(X), len(self.things)), dtype=int)
        for i, row in enumerate(X):
            for thing in row.split(self.delimiter):
                try:
                    idx = self.things.index(thing)
                    Xt[i, idx] = 1
                except ValueError:
                    pass
        return Xt

    def fit_transform(self, X):
        self.fit(X)
        Xt = self.transform(X)
        return Xt

class AdjacentNeighbors:
    def __init__(self, n=5):
        self.n = n

    def __repr__(self):
        return f'AdjacentNeighbors(n={self.n})'

    def fit(self, X):
        self.X = X
        return self

    def kneighbors(self, X, return_distance=False):
        # FIXME: there's a bug that will always return all distances
        distances = cdist(X, self.X)
        neighbors = np.argsort(distances)[:, :self.n]
        if return_distance:
            return distances, neighbors
        return neighbors
