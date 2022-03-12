from nltk.tokenize import WhitespaceTokenizer
from nltk.probability import FreqDist
from nltk.util import bigrams, trigrams
from collections import defaultdict, Counter
from random import choice, choices

with open('Game of Thrones scenario.txt', "r", encoding="utf-8") as f:
    tokens = WhitespaceTokenizer().tokenize(f.read())
    fdist = FreqDist(tokens)


def dict_of_bigrams():
    list_bigrams = list(bigrams(tokens))
    dic_tokens = defaultdict(list)
    for k, v in list_bigrams:
        dic_tokens[k].append(v)
    dic_tokens = {key: dict(Counter(value)) for key, value in dic_tokens.items()}
    return dic_tokens


def dict_of_trigrams():
    list_trigrams = list(trigrams(tokens))
    dic_tokens = defaultdict(list)
    for k, v, c in list_trigrams:
        dic_tokens[f'{k} {v}'].append(c)
    dic_tokens = {key: dict(Counter(value)) for key, value in dic_tokens.items()}
    return dic_tokens


def check_dic_tokens(index, dic_tokens):
    while index != 'exit':
        try:
            value = dic_tokens[index]
            print(f'Head: {index}')
            for tail, count in dic_tokens[index].items():
                print(f'Tail: {tail} Count: {count}')
        except KeyError:
            print('Key Error. The requested word is not in the model. Please input another word.')
        finally:
            index = input()


def first_head():
    l_text = [choice(list(dic_tokens.keys()))]
    if l_text[0].split()[0].endswith(('.', '!', '?')) or not l_text[0][0].isupper():
        while l_text[0].split()[0].endswith(('.', '!', '?')) or not l_text[0][0].isupper():
            l_text = [choice(list(dic_tokens.keys()))]
    population = list(dic_tokens[l_text[-1]].keys())
    weights = list(dic_tokens[l_text[-1]].values())
    word = choices(population, weights=weights)[0]
    l_text.append(word)
    return l_text


def sentences(l_text, dic_tokens):
    while len(l_text) < 4 or not l_text[-1].endswith(('.', '!', '?')):
        head_trigrams = f'{l_text[-2].split()[-1]} {l_text[-1]}'
        population = list(dic_tokens[head_trigrams].keys())
        weights = list(dic_tokens[head_trigrams].values())
        word = choices(population, weights=weights)[0]
        l_text.append(word)
    ready_sent = " ".join(l_text)
    print(ready_sent)


dic_tokens = dict_of_trigrams()
for i in range(10):
    head = first_head()
    sentences(head, dic_tokens)
