# Implementado según Brassard, sección 5.9
class DisjointSets:
    def __init__(self, elements):
        self.elems = list(elements)
        self.sets = list(range(len(elements)))
        self.ranks = [1] * len(elements)

    def find(self, x):
        """ Finds the label of the set containing object x. """
        i = r = self.elems.index(x)

        while self.sets[r] != r:
            # r is the root of the tree
            r = self.sets[r]
                
        while i != r:
            j = self.sets[i]
            self.sets[i] = r
            i = j

        return r

    def merge(self, a, b):
        """ Merges the sets labelled a and b; we assume a != b. """
        if self.ranks[a] == self.ranks[b]:
            self.ranks[a] = self.ranks[a] + 1
            self.sets[b] = a
        else:
            if self.ranks[a] > self.ranks[b]:
                self.sets[b] = a
            else:
                self.sets[a] = b