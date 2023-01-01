import zlib
import math
import random
import hashlib
import numpy as np


def get_random_salts(hashes_count: int):

    random_val = random.randint(10, 100)

    salts = [
        hashlib.sha224(bytes(np.random.RandomState(random_val).randint(
            0, 999_999))).hexdigest() for i in range(hashes_count)
    ]
    return salts


def get_index(word: str, salt: str, CBF_SIZE: int):
    return zlib.crc32(bytes(word + salt, encoding='utf8')) % CBF_SIZE


infelicity = 0.0001

PATH = 'example.txt'

with open(PATH, encoding="utf8") as file:
    unique_words = set(file.read().split())

NUMBER_OF_UNIQUE_WORDS = len(unique_words)

CBF_SIZE = -math.ceil((NUMBER_OF_UNIQUE_WORDS * np.log(infelicity)) / (np.log(2) ** 2))

NUMBER_OF_HASH_FUNCTIONS = round((CBF_SIZE / NUMBER_OF_UNIQUE_WORDS) * math.log(2))

cbf = [0] * CBF_SIZE
salts = get_random_salts(NUMBER_OF_HASH_FUNCTIONS)
for word in unique_words:
    for i in range(NUMBER_OF_HASH_FUNCTIONS):
        index = get_index(word=word, salt=salts[i], CBF_SIZE=CBF_SIZE)
        cbf[index] += 1

words = ['the', 'balance', 'Java', 'learning', 'build', 'coding', 'time', 'summer', 'tunnel', 'huge']

for word in words:

    minimal_val = 1000000000 - 1

    for i in range(NUMBER_OF_HASH_FUNCTIONS):
        index = get_index(word=word, salt=salts[i], CBF_SIZE=CBF_SIZE)
        if cbf[index] < minimal_val:
            minimal_val = cbf[index]

    if minimal_val > 0:
        print(f'{word}: {1 / minimal_val}')
    else:
        print(f'{word}: 0')
