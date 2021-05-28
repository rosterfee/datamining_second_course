import random
import copy

baskets = []
products_words = ['bread', 'milk', 'cheese', 'eggs', 'coke', 'butter', 'beer', 'apples', 'chips', 'meat']
products = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

for i in range(100):
    basket = []
    products_count = random.randint(1, len(products))
    for j in range(products_count):
        random_product = random.choice(products)
        if random_product not in basket:
            basket.append(random_product)
    baskets.append(basket)

singleton_map = {}
for basket in baskets:
    for product in basket:
        if product in singleton_map:
            singleton_map[product] += 1
        else:
            singleton_map[product] = 1

singletons_support_number = 0
for product_count in singleton_map.values():
    singletons_support_number += product_count
singletons_support_number /= len(products)
singletons_support_number *= 0.8

singletons_blacklist = []
for product, count in singleton_map.items():
    if count < singletons_support_number:
        singletons_blacklist.append(product)
print(f'blacklist: {singletons_blacklist}')

doubletons = []
for basket in baskets:
    for i in range(len(basket)):
        for j in range(i + 1, len(basket)):
            first_product = min(basket[i], basket[j])
            second_product = max(basket[i], basket[j])

            doubleton = [first_product, second_product]

            doubletons.append(doubleton)

print(f'before: {len(doubletons)}')
for koef in range(1, 3):
    hash_buckets_map = {}
    for doubleton in doubletons:
        hash = (doubleton[0] + koef * doubleton[1]) % len(products)
        if hash in hash_buckets_map:
            hash_buckets_map[hash].append(doubleton)
        else:
            hash_buckets_map[hash] = [doubleton]

    doubletons_support_number = 0
    for doubletons in hash_buckets_map.values():
        doubletons_support_number += len(doubletons)
    doubletons_support_number /= len(products)
    doubletons_support_number *= 0.8

    for doubletons_list in hash_buckets_map.values():
        if len(doubletons_list) < doubletons_support_number:
            for doubleton in doubletons_list:
                while doubleton in doubletons:
                    doubletons.remove(doubleton)

    print(f'after: {len(doubletons)}')

result_doubletons = copy.deepcopy(doubletons)
print(result_doubletons)
for product in singletons_blacklist:
    for doubleton in doubletons:
        if product in doubleton:
            while result_doubletons.__contains__(doubleton):
                result_doubletons.remove(doubleton)

print('Выявленные комбинации:')
for product in products:
    if product not in singletons_blacklist:
        print(products_words[product])

result_doubletons_set = copy.deepcopy(result_doubletons)
for doubleton in result_doubletons:

    print(f'{products_words[doubleton[0]]} часто покупают с {products_words[doubleton[1]]}')
