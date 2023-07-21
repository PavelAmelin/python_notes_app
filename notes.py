import json
from datetime import datetime as dt

def load_file(f_name):
    with open(f_name, 'r', encoding='utf-8') as file:
        d = json.load(file)
    return d

def add_note(dct):
    id_add = input('Введите ID для добавления: ')
    head = input('Введите заголовок заметки: ')
    body = input('Введите заметку: ')
    dct[id_add] = head, body, dt.now().strftime('%Y.%m.%d %H:%M:%S')
    dct = load_file('notes.json')
    if id_add not in dct:
        dct[id_add] = head, body, dt.now().strftime('%Y.%m.%d %H:%M:%S')
    else:
        print('Такой ID уже существует')
        add_note(dct)
    with open('notes.json', 'w', encoding='utf-8') as file:
        json.dump(dct, file, indent=3)


def del_note(filename):
    try:
        id_del = input('Введите ID для удаления: ')
        data = load_file(filename)
        data.pop(id_del)
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=3)
        print('Заметка удалена, файл notes.json перезаписан')
    except KeyError:
        print('Такого ID не существует')


def edit_note(filename):
    id_edit = input('Введите ID для редактирования: ')
    head = input('Введите новый заголовок заметки: ')
    body = input('Введите новую заметку: ')
    data = load_file(filename)
    if id_edit in data:
        data[id_edit] = head, body, dt.now().strftime('%Y.%m.%d %H:%M:%S')
        print('Заметка изменена, файл notes.json перезаписан')
    else:
        print('Такого ID не существует')
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=3)


def read_from_json(filename):
    try:
        data = load_file(filename)
        pat = '%Y.%m.%d %H:%M:%S'
        data_min_str = input(
            'Введите минимальную дату (в формате год.месяц.день часы:минуты:секунды XXXX.XX.XX XX:XX:XX): ')
        data_max_str = input(
            'Введите максимальную дату (в формате год.месяц.день часы:минуты:секунды XXXX.XX.XX XX:XX:XX): ')
        data_min = dt.strptime(data_min_str, pat)
        data_max = dt.strptime(data_max_str, pat)
        all_notes = dict(filter(lambda x: data_min <= dt.strptime(x[1][2], pat) <= data_max, data.items()))
        for k, v in all_notes.items():
            print(k, ';'.join(v), sep=';')
        print('Файл прочитан с фильтрацией по датам, между которыми были сделаны заметки')
    except ValueError:
        print('Дату ввести строго в том формате в котором указано')


def print_note(filename):
    try:
        id_print = input('Введите ID записи: ')
        data = load_file(filename)
        print(id_print, ';'.join(data[id_print]), sep=';')
    except KeyError:
        print('Такого ID не существует')


res = {}
while True:
    print('''add - добавление заметки; del - удаление заметки; edit - редактирование заметки; rd - чтение 
    заметок из файла с фильтрацией по датам, между которыми были сделаны заметки; id - вывод заметки по ID''')
    command = input('Введите комманду add, del, edit, rd, id или end для завершения работы: ')
    if command == 'add':
        add_note(res)
        print('Заметка добавлена в журнал, файл notes.json перезаписан')
    elif command == 'del':
        del_note('notes.json')
    elif command == 'edit':
        edit_note('notes.json')
    elif command == 'rd':
        read_from_json('notes.json')
    elif command == 'id':
        print_note('notes.json')
    elif command == 'end':
        break
    else:
        print('можно вводить только комманды add, del, edit, rd, id или end')