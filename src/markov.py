import os
import random

from .const import MAX_LENGTH
from .utils import check_content
from .graph import WordGraph

PROMPT = 'Somebody' # once told me, the world was gonna roll me..

def create_training_set(dir):
    training_set = ''
    for filename in os.listdir(dir):
        file = os.path.join(dir, filename)

        assert os.path.isfile(file)
        assert filename[-4:] == '.txt'

        with open(file, 'r') as f:
            line = f.read()
            training_set += line # or line.lower() if you want case-agnostic

    # clean data
    training_set = training_set.replace('\n',' ')
    training_set = training_set.replace('\t',' ')
    training_set = training_set.replace('“', ' ')
    training_set = training_set.replace('”', ' ')
    training_set = training_set.replace('(', ' ')
    training_set = training_set.replace(')', ' ')

    for spaced in ['.', '-', ',', '!', '?', '(', '—', ')']:
        training_set = training_set.replace(spaced, f' {spaced} ')

    training_set = training_set.split(' ')

    return training_set

def build_word_graph(training_set):
    size = len(training_set)
    word_graph = WordGraph.get_instance()

    i = 0
    while i < size - 1:
        word = training_set[i]
        next_word = training_set[i + 1]
        word_graph.add(word, next_word)
        i += 1
    word_graph.save()
    return word_graph

def build_two_word_graph(training_set):
    size = len(training_set)
    word_graph = WordGraph.get_instance()

    i = 0
    prev_word = None
    while i < size - 1:
        word = training_set[i]
        next_word = training_set[i + 1]

        if prev_word is None: word_graph.add(word, next_word)
        else: word_graph.add(f'{prev_word} {word}', next_word)

        prev_word = word
        i += 1
    word_graph.save()
    return word_graph

def generate_text(word_graph, prompt):
    text = [prompt]

    while prompt != '.' or len(text) < MAX_LENGTH:
        options = word_graph.get(prompt)

        if options: words, weights = options.get_dist()
        else: return "Error: Sorry, your prompt isn't in the graph."

        if len(words) > 0:
            prompt = random.choices(words, weights=weights, k=1)[0]
            text.append(prompt)
        else: break

    text = ' '.join(text)
    return text


def train(dir='data'):
    training_set = create_training_set(dir)
    word_graph = build_word_graph(training_set)



def load_response(prompt=PROMPT):
    """Building custom responses based on stored content."""

    train()
    word_graph = WordGraph.load()

    response = generate_text(word_graph, prompt=prompt)
    if check_content(response): return response
    else: raise Exception("Unsafe content... result contained expletives.")
