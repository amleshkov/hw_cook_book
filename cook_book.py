import unittest
from collections import defaultdict

cook_book = defaultdict(list)


def parser(line: str) -> dict:
    parsed_line = line.split(" | ")
    return {'ingredient_name': parsed_line[0], 'quantity': parsed_line[1], 'measure': parsed_line[2]}


def enrich_book(entry: list) -> None:
    cook_book[entry[0]] = [parser(el) for el in entry[2:]]


def get_shop_list_by_dishes(dishes: list, person_count: int) -> dict:
    result = {}
    for dish in dishes:
        ingredients = cook_book[dish]
        for ingredient in ingredients:
            key = ingredient['ingredient_name']
            quantity = int(ingredient['quantity'])
            measure = ingredient['measure']
            if key in result:
                result[key]['quantity'] += quantity * person_count
            else:
                result[key] = {'measure': measure, 'quantity': quantity * person_count}
    return result


class TestParsing(unittest.TestCase):

    def setUp(self):

        with open("recipes.txt") as f:
            entry = []
            for line in f:
                line = line.strip()
                if line:
                    entry.append(line)
                else:
                    enrich_book(entry)
                    entry = []
            else:
                # последне блюдо в примере на заканчивается пустой строкой, но его все равно нужно записать в cook_book
                enrich_book(entry)

    def test_parsing(self):
        expected_cook_book = {'Омлет': [{'ingredient_name': 'Яйцо', 'quantity': '2', 'measure': 'шт'},
        {'ingredient_name': 'Молоко', 'quantity': '100', 'measure': 'мл'},
        {'ingredient_name': 'Помидор', 'quantity': '2', 'measure': 'шт'}],
        'Утка по-пекински': [{'ingredient_name': 'Утка',
        'quantity': '1',
        'measure': 'шт'},
        {'ingredient_name': 'Вода', 'quantity': '2', 'measure': 'л'},
        {'ingredient_name': 'Мед', 'quantity': '3', 'measure': 'ст.л'},
        {'ingredient_name': 'Соевый соус', 'quantity': '60', 'measure': 'мл'}],
        'Запеченный картофель': [{'ingredient_name': 'Картофель',
            'quantity': '1',
            'measure': 'кг'},
        {'ingredient_name': 'Чеснок', 'quantity': '3', 'measure': 'зубч'},
        {'ingredient_name': 'Сыр гауда', 'quantity': '100', 'measure': 'г'}],
            'Фахитос': [{'ingredient_name': 'Говядина',
            'quantity': '500',
            'measure': 'г'},
        {'ingredient_name': 'Перец сладкий', 'quantity': '1', 'measure': 'шт'},
        {'ingredient_name': 'Лаваш', 'quantity': '2', 'measure': 'шт'},
        {'ingredient_name': 'Винный уксус', 'quantity': '1', 'measure': 'ст.л'},
        {'ingredient_name': 'Помидор', 'quantity': '2', 'measure': 'шт'}]}

        self.assertEqual(cook_book, expected_cook_book)

    def test_get_shop_list_by_dishes(self):
        expected_with_two_persons = {'Картофель': {'measure': 'кг', 'quantity': 2},
        'Чеснок': {'measure': 'зубч', 'quantity': 6},
        'Сыр гауда': {'measure': 'г', 'quantity': 200},
        'Яйцо': {'measure': 'шт', 'quantity': 4},
        'Молоко': {'measure': 'мл', 'quantity': 200},
        'Помидор': {'measure': 'шт', 'quantity': 4}}

        expected_with_duplicate_ingredients = {'Говядина': {'measure': 'г', 'quantity': 500},
        'Перец сладкий': {'measure': 'шт', 'quantity': 1},
        'Лаваш': {'measure': 'шт', 'quantity': 2},
        'Винный уксус': {'measure': 'ст.л', 'quantity': 1},
        'Помидор': {'measure': 'шт', 'quantity': 4},
        'Яйцо': {'measure': 'шт', 'quantity': 2},
        'Молоко': {'measure': 'мл', 'quantity': 100}}

        self.assertEqual(get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2),
                         expected_with_two_persons)
        self.assertEqual(get_shop_list_by_dishes(['Фахитос', 'Омлет'], 1),
                         expected_with_duplicate_ingredients)
