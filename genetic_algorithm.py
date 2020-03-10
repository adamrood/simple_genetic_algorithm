import string
import numpy as np
import pandas as pd
from collections import Counter
import sys
import time
import matplotlib.pyplot as plt

def create_population(n):
    global df
    pop = []
    for x in range(n):
        pop.append(''.join(np.random.choice([x for x in string.printable[:62]], len(key))))
    df = pd.DataFrame(pop,columns=['key'])
    df['score'] = cost_function(pop)
    df['prob'] = pd.Series(df['score'])/sum(pd.Series(df['score']))

def cost_function(value):
    global scores
    scores = []
    for x in range(len(value)):
        counter = 0
        for y in range(len(key)):
            if (key[y] == value[x][y]):
                counter += 1
        scores.append(counter)
    return scores

def crossover(df, threshold, mutation_rate):
    global new_population, p_a, p_b, p_o
    parents = np.random.choice(df['key'], size = 2, p = df['prob'], replace = False)
    slicers = np.random.randint(0,len(key),2)
    thresh = np.random.uniform(0,1,1)
    if thresh <= threshold:
        for x in slicers:
            p_a = parents[0][0:x]
            p_b = parents[1][x:]
            p_o = p_a + p_b
            mutation(mutation_rate)
    new_population.append(p_o)

def mutation(rate):
    global p_o, p_o_list, max_score
    if np.random.choice([0,1], size = 1, p = [1 - rate, rate]) == 1:
        char = str(np.random.choice([x for x in string.printable[:62]], 1).item(0))
        index = int(np.random.randint(0,len(key),1))
        p_o_list = list(p_o)
        p_o_list[index] = char
        p_o = ''.join(p_o_list)

def breed(pop_size, mutation_rate):
    global df, new_population, max_score
    new_population = []
    for x in range(pop_size):
        try:
            crossover(df,0.90,mutation_rate)
        except:
            create_population(pop_size)
            crossover(df,0.90,mutation_rate)
    df['key'] = new_population
    df['score'] = cost_function(new_population)
    df['prob'] = pd.Series(df['score'])/sum(pd.Series(df['score']))
    max_score = max(df['score'])

def create_key(key_size):
    key = ''.join(np.random.choice([x for x in string.printable[:62]], key_size))
    return key

key_length = 16
population_size = 1000
mutation_rate = 0.02
key = create_key(key_length)
create_population(population_size)
counter = 0
print('The key is: ', key)
max_score = 0
while max(df['score']) != key_length:
    breed(population_size,mutation_rate)
    counter += 1
    max_score_temp = max_score
    max_score = max(df['score'])
    best_string = max(df.loc[df['score'] == max(df['score']), 'key'])
    best_score = max(df.loc[df['score'] == max(df['score']), 'score'])
    sys.stdout.write("\r" + 'Solving...:  ' + best_string + '  (' + str(best_score) + ', ' + str(counter) + ')')
    sys.stdout.flush()
    if counter <= 100:
        continue
    else:
        next
print()
print('')
print('It took',counter,'iterations to crack the code!')