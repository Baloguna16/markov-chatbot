import os
import pickle

class WordGraph:
    _instance = None
    _dir = 'src/pickle'
    _filename = 'word_graph.pickle'

    def __init__(self):
        singleton_error = 'Graph should only be created once.'
        assert WordGraph._instance is None, singleton_error

        self._set = {}
        WordGraph._instance = self

    @staticmethod
    def get_instance():
        if WordGraph._instance is None:
            WordGraph()
        return WordGraph._instance


    def add(self, word, next_word):
        if self._set.get(word) is None:
            adj_list = AdjacencyList()
            adj_list.insert(next_word)
        else:
            adj_list = self._set[word]
            adj_list.insert(next_word)

        self._set[word] = adj_list

    def get(self, word, silent_fail=False):
        adj_list = self._set.get(word)
        if silent_fail: assert adj_list
        return adj_list

    @staticmethod
    def load():
        file = os.path.join(WordGraph._dir, WordGraph._filename)
        with open(file, 'rb') as f: word_graph = pickle.load(f)
        return word_graph

    def save(self):
        file = os.path.join(WordGraph._dir, WordGraph._filename)
        with open(file, 'wb') as f: pickle.dump(self._instance, f)

class AdjacencyList:

    def __init__(self):
        self.global_count = 0
        self.size = 0
        self._adj = {}

    def insert(self, word):
        if self._adj.get(word):
            self._adj[word] += 1
        else:
            self._adj[word] = 1
            self.size += 1
        self.global_count += 1

    def get_dist(self):
        words = []
        weights = []
        for word, count in self._adj.items():
            probability = count / self.global_count
            words.append(word)
            weights.append(probability)
        return words, weights
