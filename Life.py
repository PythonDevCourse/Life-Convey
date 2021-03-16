"""Эта программа - реализация игры Конвея под названием 'Жизнь'. В игре
есть поле, завёрнутое в 'бублик'. В игре есть живые клетки и мёртвые.
Правила игры:
    Клетка умирает, если у неё либо меньше 2 соседей, либо больше 3
    Мёртвая клетка оживает, если у неё ровно 3 соседа
Игра заканчивается, если:
    Не останется ни одной клетки
    Если следующая генерация повторит себя в прошлом ходу
    Если генерация повторит себя за несколько ходов назад
Тебе понравится!"""
import time
import doctest

from representation import field
from constants import COORD_MAX_X, COORD_MAX_Y, SIZE_OF_THE_CELL_X, SIZE_OF_THE_CELL_Y

initial = [(35,34), (35,35), (35,36), (36,36)]

def is_alive(y, x, generation):
    """Принимает местоположение клетки(x, y), и список всех генераций
    Выводит жива она, или нет"""
    try:
        more_than_max(y, x, generation)
        generation.index((y, x))
        return True
    except ValueError:
        return False
    return False

def calc_neighbours(y, x, generation):
    """
    Принимает местоположение клетки(x, y), и список всех генераций
    Выводит количество соседей
    >>> calc_neighbours(3, 3, [(3,4), (3,3), (3,2)])
    2
    """
    alive_neighbours = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i==0 and j==0:
                continue
            if is_alive(y+i, x+j, generation):     
                alive_neighbours +=1
    return alive_neighbours
        
def is_born(y, x, generation):
    """Принимает местоположение клетки(x, y), и список всех генераций
    Выводит жива она или нет"""
    neighbours = calc_neighbours(y, x, generation)
    if neighbours == 3:
        return True

def find_new_life(y,x, generation):
    """
    Принимает местоположение клетки(x, y), и список всех генераций
    Выводит список всех новорождённых клеток
    >>> find_new_life(3, 3, [(3,4), (3,3), (3,2)])
    [(2, 3), (4, 3)]
    """
    newborn_cells = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if is_born(y+i, x+j, generation):
                newborn_cells.append((y+i, x+j))
    return newborn_cells

def more_than_max(y, x, generation):
    """
    Принимает местоположение клетки(x, y), и список всех генераций
    Проводит местоположение по габаритам
    Выводит усовершенствованные параметры
    >>> more_than_max(-1, 701,[(3, 2), (3, 3), (3, 4)])
    (699, 1)
    """
    
        
    if x < 0 or y < 0 or x > COORD_MAX_X or y > COORD_MAX_Y:
        if x < 0:
            x = COORD_MAX_X + x 
        if y < 0:
            y = COORD_MAX_Y + y 
        if x > COORD_MAX_X:
            x = x - COORD_MAX_X
        if y > COORD_MAX_Y:
            y = y - COORD_MAX_Y
    return y, x

def calc_generation(generation):
    """Принимает список всех генераций
    Выводит новые генерации
    >>> calc_generation([(3, 2), (3, 3), (3, 4)])
    [(2, 3), (3, 3), (4, 3)]
    """
    new_generation = []
    for (y, x) in generation:
        non = calc_neighbours(x, y, generation)
        
        if non >= 2 and non <= 3:
            new_generation.append((x, y))

        new_generation.extend(find_new_life(x, y, generation))        
    
    return list(set(new_generation))

def check(spisok: list):
    """
    Принимает список поколений с дубликатами/без дубликатов
    Выводит есть ли там дубликаты, или нет
    #>>> check([(3, 2), (3, 2)])
    False
    #>>> check([(3, 2), (3, 3)])
    True
    """
    spisok = spisok.reverse
    if spisok[0] == spisok[1]:
        spisok = spisok.reverse
        return False
    else:
        return True

def main():
    """Основная функция"""
    generatios = []
    state = initial
    generatios.append(tuple(state))
    while len(state) > 0:
        state = generatios[-1]
        state = calc_generation(state)
        field(state)
        time.sleep(0.5)
        generatios.append(tuple(state))

        print(generatios)
        

if __name__ == "__main__":
    # doctest.testmod()
    main()