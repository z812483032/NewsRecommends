from .utils import ThingVectorizer, AdjacentNeighbors

class Recommend:
    def __init__(self, n=5, delimiter=',', max_things=None):
        self.tv = ThingVectorizer(delimiter, max_things)
        self.an = AdjacentNeighbors(n)

    def __repr__(self):
        return f'Recommend(n={self.an.n}, delimiter="{self.tv.delimiter}", max_things={self.tv.max_things})'

    def fit(self, X):
        self.X = X
        X = self.tv.fit_transform(X)
        self.an.fit(X)
        return self

    def predict(self, X):
        Xp = []
        for Xi in X:
            Xt = self.tv.transform([Xi])
            neighbors = self.an.kneighbors(Xt)
            things = []
            for n in neighbors[0]:
                t = self.X.iloc[int(n)].split(",")
                things.extend(t)
            things = list(set(things))
            things = [t for t in things if t not in Xi.split(",")]
            Xp.append(things)
        return Xp
