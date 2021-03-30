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

    # Возвращаю сфоромированный одномерный словарь ссылок
    return dic


# Получаю двумерный словарь (dic[A][B] == пересечение A и B в матрице, то есть вес) из
# рекурсивного метода (глубина = 3)
dic = generate_map(url=URL, depth=3, dic={}, level=1)

# Создаю матрицу на основе двумерного словаря из одномерного словаря
matrix = {}
for key1, links in dic.items():
    matrix[key1] = {}
    for key2 in dic.keys():
        # Если есть переход со страницы A на страницу B, формирую вес: число ссылок на B делю на общее
        # кол-во ссылок на странице A
        if key2 in links:
            matrix[key1][key2] = links.count(key2) / len(links)
        # Если перехода нет, то вес = 0
        else:
            matrix[key1][key2] = 0

# Создаю направленный взвешенный граф с помощью библиотеки networkX
graph = nx.MultiDiGraph()

# Добавляю дуги в граф
for key, value in dic.items():
    for link in value:
        graph.add_edge(key, link, weight=value.count(link) / len(value))

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

for key, value in dic.items():
    if len(value) == 0:
        del matrix[key]
        for string, columns in matrix.items():
            if key in columns:
                del matrix[string][key]

# Создаю начальный вектор
init_vector = {}
for key in matrix.keys():
    init_vector[key] = 1 / len(matrix)

# Перемножаю матрицу на вектор n раз, на выходе получаю page rank вектор
page_rank_vector = {}
for i in range(1):
    for string, columns in matrix.items():
        sum = 0
        for column, weight in columns.items():
            sum += weight * init_vector[column]
        page_rank_vector[string] = sum

    init_vector = copy.deepcopy(page_rank_vector)

# Формирую список всех ссылок (неповторяющихся), которые понадобятся, чтобы посчитать page rank of dead ends
all_links = set()
for key, value in dic.items():
    print(key + ": " + str(value))
    for i in value:
        all_links.add(i)

# Считаю page rank для dead ends
for link in all_links:
    if link not in page_rank_vector.keys():
        page_rank_vector[link] = 0
        for key, links in dic.items():
            if link in links:
                page_rank_vector[link] += page_rank_vector[key] * (links.count(link) / len(links))

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
