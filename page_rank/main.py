import requests
import re
import networkx as nx
import matplotlib.pyplot as plt
import copy

from bs4 import BeautifulSoup

URL = "https://spring.io/"


# Метод, который рекурсивно генерирует одномерный словарь отношений ссылок в зависимости от заданной глубины
def generate_map(url: str, depth: int, dic: dict, level):
    while url.endswith("/"):
        url = url.rstrip("/")

    dic[url] = []
    links: list = dic[url]

    # Получаю страницу по адресу
    page = requests.get(url)
    html = page.text

    # Вычленяю доменное имя для формировния полных uri адресов(есть ссылки типа /products и т.д.)
    if url.count("/") > 2:
        if url.startswith("http:"):
            regex = 'http://(.*)/'
        else:
            regex = 'https://(.*)/'
        domen = re.search(regex, url).group(1).split("/")[0]
    else:
        if url.startswith('http:'):
            domen = url[url.find('http://') + 7:]
        else:
            domen = url[url.find('https://') + 8:]

        question_mark_position = domen.find('?')
        if question_mark_position != -1:
            domen = domen[:question_mark_position]

    # Создаю парсер для страницы
    soup = BeautifulSoup(html, features='html.parser')

    # Достаю теги <a>, затем у них атрибут href, добавляю в словарь все ссылки и, если глубина не
    # достигнута, иду еще глубже для каждой ссылки
    tags = soup.select(selector='a')
    for i in tags:
        attributes = i.attrs
        if 'href' in attributes:
            link = attributes['href']
            if not link.startswith('#'):
                if not link.startswith("http"):
                    link = "https://" + domen + link
                while link.endswith('/'):
                    link = link.rstrip('/')
                links.append(link)
                if dic.get(link) is None and level < depth:
                    generate_map(url=link, depth=depth, dic=dic, level=level + 1)

    # Возвращаю сформированный одномерный словарь ссылок
    return dic


def get_page_rank(link: str, matrix: dict, page_rank_vector: dict):
    if link in page_rank_vector.keys():
        return page_rank_vector[link]
    else:
        sum = 0
        for string in matrix.keys():
            if matrix[string][link] != 0:
                print('string: ' + string)
                sum += get_page_rank(link=string, matrix=matrix, page_rank_vector=page_rank_vector) * matrix[string][link]
        print('link: ' + link)
        page_rank_vector[link] = sum

        return sum


def copy_matrix_with_zeros(matrix: dict):
    result_matrix = {}
    for string, columns in matrix.items():
        result_matrix[string] = {}
        for column, weight in columns.items():
            result_matrix[string][column] = 0
    return result_matrix


# Получаю двумерный словарь (dic[A][B] == пересечение A и B в матрице, то есть вес) из
# рекурсивного метода (глубина = 3)
dic = generate_map(url=URL, depth=1, dic={}, level=1)

# Создаю направленный взвешенный граф с помощью библиотеки networkX
graph = nx.MultiDiGraph()

# Добавляю дуги в граф
for key, value in dic.items():
    for link in set(value):
        graph.add_edge(key, link)

# Настраиваю стили для визуализации графа
options = {
    'node_color': 'red',
    'node_size': 10,
    'edge_color': 'blue',
    'width': 0.05
}

# Визуализирую граф
nx.draw_random(graph, with_labels=False, **options)
plt.show()

# Формирую список всех ссылок (неповторяющихся), которые понадобятся, чтобы посчитать page rank of dead ends
all_links = set()
for key, value in dic.items():
    for i in value:
        all_links.add(i)
print(all_links)

# Создаю матрицу на основе двумерного словаря из одномерного словаря
matrix = {}
for link1 in all_links:
    matrix[link1] = {}
    for link2 in all_links:
        if link1 in dic:
            links = dic[link1]
            # Если есть переход со страницы A на страницу B, формирую вес: число ссылок на B делю на общее
            # кол-во ссылок на странице A
            if len(links) != 0:
                matrix[link1][link2] = links.count(link2) / len(links)
            # Если перехода нет, то вес = 0
            else:
                matrix[link1][link2] = 0
        else:
            matrix[link1][link2] = 0

for string, columns in matrix.items():
    for column, weight in columns.items():
        print(string + ": " + column, end=' ')
    print('\n')

corrected_matrix = {}
for key1, value1 in dic.items():
    if len(value1) != 0:
        corrected_matrix[key1] = {}
        for key2, value2 in dic.items():
            if len(value2) != 0:
                corrected_matrix[key1][key2] = matrix[key1][key2]

for string, columns in corrected_matrix.items():
    for column, weight in columns.items():
        print("corrected matrix: " + string + ": " + column)

# /**
result_matrix = copy_matrix_with_zeros(corrected_matrix)
for i in range(1):

    for key1 in corrected_matrix.keys():
        for value in corrected_matrix[key1].keys():
            for key2 in corrected_matrix.keys():
                result_matrix[key1][value] += corrected_matrix[key1][key2] * corrected_matrix[key2][value]

    corrected_matrix = copy.deepcopy(result_matrix)
    result_matrix = copy_matrix_with_zeros(corrected_matrix)

init_vector = {}
for key in corrected_matrix.keys():
    init_vector[key] = 1 / len(corrected_matrix)

page_rank_vector = {}
for string, columns in corrected_matrix.items():
    sum = 0
    for column, weight in columns.items():
        sum += weight * init_vector[column]
    page_rank_vector[string] = sum
# /**

for link in all_links:
    print(link)
    page_rank_vector = get_page_rank(link=link, matrix=matrix, page_rank_vector=page_rank_vector)

# Сортирую page rank вектор по убыванию ранга
sorted_page_rank_vector = {}
sorted_links = sorted(page_rank_vector, key=page_rank_vector.get)
for link in sorted_links:
    sorted_page_rank_vector[link] = page_rank_vector[link]

# Распечатываю 10 самых ранжированных страниц
print('10 самых ранжированных страниц:')
counter = 0
for link, page_rank in reversed(sorted_page_rank_vector.items()):
    if counter < 10:
        print(f'{link}: {page_rank}')
        counter = counter + 1

print(f'Всего страниц: {len(all_links)}')

sum = 0
for key, value in sorted_page_rank_vector.items():
    sum += value

print(sum)
