import random


# Функция, которая возвращает второй момент по алгоритму
def calc_second_moment(arr: [], vars_count: int, arr_size: int):

    # Создаю список из рандомных индексов переменных в массиве
    vars_indexes = []
    for i in range(vars_count):
        vars_indexes.append(random.randint(0, arr_size - 1))
    vars_indexes = sorted(vars_indexes)

    # Словарь для подсчета количества вхождений каждого числа
    map = {}

    # Прохожусь по каждому индексу
    for var_index in vars_indexes:

        # Беру число в массиве по индексу. Если оно уже есть в качестве ключа в словаре,
        # перебираю индексы правее данного
        while arr[var_index] in map and var_index < arr_size - 1:
            var_index += 1

        # Если даже после перебора не нашлось числа, которого нет в качестве ключа в словаре,
        # ничего не делаю, иначе выполняю подсчет количества вхождений числа в массив
        if arr[var_index] not in map:
            # Фиксирую число
            current_num = arr[var_index]
            map[current_num] = 1
            # Делаю проверку, не дошли ли мы до конца массива
            if var_index + 1 < arr_size:
                # Если не дошли, перебираю все числа, правее зафиксированного и считаю
                # количество вхождений
                for i in range(var_index + 1, arr_size):
                    if current_num == arr[i]:
                        map[current_num] += 1

    # Ввожу переменную для подсчета второго момента
    second_moment = 0
    # Считаю второй момент по формуле: moment = (∑N(2*Mi-1))/n, где N-размер потока,
    # Mi-количество вхождений i-го числа в поток, n-количество переменных
    for value in map.values():
        second_moment += arr_size * (2 * value - 1)
    second_moment /= len(map)

    # Возвращаю второй момент, посчитанный по алгоритму
    return second_moment


# Создаю массив и заполняю его рандомными числами
arr = []
for i in range(1000000):
    arr.append(random.randint(1, 1000))

# Нулевой момент - это количество уникальных чисел в потоке
set = set(arr)
print(f'Нулевой момент: {len(set)}')

# Считаю количество вхождений каждого числа в потоке
dic = {}
for i in arr:
    if i in dic:
        dic[i] += 1
    else:
        dic[i] = 1

# Считаю первый момент
sum = 0
for value in dic.values():
    sum += value

print(f'Первый момент: {sum}')

# Считаю точный второй момент
sum = 0
for value in dic.values():
    sum += value ** 2

print(f'Точный второй момент: {sum}')

second_moment = calc_second_moment(arr=arr, vars_count=100, arr_size=1000000)
print(f'Второй момент со 100 переменными по алгоритму: {second_moment}')

second_moment = calc_second_moment(arr=arr, vars_count=500, arr_size=1000000)
print(f'Второй момент с 500 переменными по алгоритму: {second_moment}')