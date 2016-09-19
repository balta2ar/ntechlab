"""
This method implements basic unit tests for KDTreeModel.

It also includes basic performance test and a test that compares the output
of naive and opitmized get_nearest methods.
"""
from unittest import TestCase
from random import random
from random import randint
from random import choice
from string import ascii_letters
from timeit import timeit
from time import time

from model import KDTreeModel


def generate_model(model, n):
    print('Generating %d items' % n)
    start = time()
    for i in range(n):
        x = 100000. * random()
        y = 100000. * random()
        name = ''.join([choice(ascii_letters) for _ in range(5)])
        age = randint(0, 100)
        model.create_user(x, y, name, age, rebuild_model=False)
    model.rebuild_model()
    delta = time() - start
    print('Done generating %d items (%.1fs)' % (n, delta))
    return delta


class CustomTestCase(TestCase):
    def setUp(self):
        self.model = KDTreeModel()


class TestGetNearestToyData(CustomTestCase):
    def setUp(self):
        self.model = KDTreeModel()
        self.model.create_user(1, 1, 'John', 20)
        self.model.create_user(2, 1, 'Mark', 30)
        self.model.create_user(3, 1, 'Randy', 40)
        self.model.create_user(4, 1, 'Alex', 50)
        self.model.create_user(5, 1, 'Hue', 60)

    def test_one_neighbor(self):
        user = self.model.get_user(0)
        self.assertEqual('John', user['name'])
        nearest = self.model.get_nearest(user_id=0, k_neighbors=1, radius=5)
        self.assertEqual('Mark', nearest[0]['name'])
        self.assertEqual(1, len(nearest))

    def test_k_greater_than_n(self):
        nearest = self.model.get_nearest(user_id=0, k_neighbors=5, radius=5)
        self.assertEqual('Mark', nearest[0]['name'])
        self.assertEqual(4, len(nearest))

    def test_two_users_limit_by_radius(self):
        nearest = self.model.get_nearest(user_id=0, k_neighbors=10, radius=2.5)
        self.assertEqual(2, len(nearest))

    def test_two_users_limit_by_k(self):
        nearest = self.model.get_nearest(user_id=0, k_neighbors=2, radius=10)
        self.assertEqual(2, len(nearest))

    def test_no_users_too_small_radius(self):
        nearest = self.model.get_nearest(user_id=0, k_neighbors=5, radius=0.5)
        self.assertEqual(0, len(nearest))

    def test_no_users_too_small_k(self):
        nearest = self.model.get_nearest(user_id=0, k_neighbors=0, radius=5)
        self.assertEqual(0, len(nearest))

    def test_nearest_after_delete(self):
        self.model.delete_user(0)
        nearest = self.model.get_nearest(user_id=1, k_neighbors=5, radius=10)
        self.assertEqual('Randy', nearest[0]['name'])
        self.assertEqual(3, len(nearest))


class TestCRUD(CustomTestCase):
    def test_create_and_get(self):
        user_id = self.model.create_user(1, 1, 'John', 20)
        self.assertFalse(self.model.is_present(999))
        self.assertTrue(self.model.is_present(user_id))
        self.assertDictEqual({'x': 1, 'y': 1, 'name': 'John', 'age': 20},
                             self.model.get_user(user_id))

    def test_remove(self):
        user_id1 = self.model.create_user(1, 1, 'John', 20)
        user_id2 = self.model.create_user(2, 1, 'Mark', 21)
        self.model.delete_user(user_id1)

        self.assertFalse(self.model.is_present(user_id1))
        self.assertTrue(self.model.is_present(user_id2))

    def test_update(self):
        user_id1 = self.model.create_user(1, 1, 'John', 20)
        user_id2 = self.model.create_user(2, 1, 'Mark', 30)
        user_id3 = self.model.create_user(3, 1, 'Randy', 40)

        self.model.update_user(user_id2, 10, 20, 'Sam', 50)

        self.assertDictEqual({'x': 1, 'y': 1, 'name': 'John', 'age': 20},
                             self.model.get_user(user_id1))
        self.assertDictEqual({'x': 10, 'y': 20, 'name': 'Sam', 'age': 50},
                             self.model.get_user(user_id2))
        self.assertDictEqual({'x': 3, 'y': 1, 'name': 'Randy', 'age': 40},
                             self.model.get_user(user_id3))


class TestPerformance(CustomTestCase):
    def test_performance(self):
        num_runs = 1000
        k_neighbors = 5
        radius = 5

        for data_size in (100, 1000, 10000, 100000, 1000000):
            self.model.reset()
            generate_model(self.model, data_size)
            print('Measuring...')
            result = timeit(lambda: self.model.get_nearest(user_id=0,
                                                           k_neighbors=k_neighbors,
                                                           radius=radius),
                            number=num_runs)
            print('\n%d items: get_nearest takes %.05fs for %d runs' % (data_size, result, num_runs))


class TestCompareNaiveAndFastOutput(CustomTestCase):
    def test_get_nearest_result(self):
        num_runs = 1000
        k_neighbors = 5
        radius = 5
        data_size = 1000

        self.model.reset()
        generate_model(self.model, data_size)

        for i in range(data_size):
            result_fast = self.model.get_nearest(user_id=i,
                                                 k_neighbors=k_neighbors,
                                                 radius=radius)
            result_slow = self.model.get_nearest_naive(user_id=i,
                                                       k_neighbors=k_neighbors,
                                                       radius=radius)
            self.assertEqual(result_fast, result_slow)
