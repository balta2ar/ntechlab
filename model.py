"""
This module implements KDTreeModel that allows for retrieval of K nearest
neighbors within a given radius R.

KDTreeModel implements two methods to retrieve neighbors. Naive method linearly
scans all users and computes distance from each user to current user. Users
that are within the given radius are tracked in a heap of size K.

Optimized method facilitates cKDTree from scipy to retrieve neighbors faster.
The price for this is memory overhead of auxiliry data structures. As long
as it is implied from the problem description that the main purpose of the
service is to be good at retrieving neighbors, the use of the optimized method
is recommended.
"""
from heapq import heappush
from heapq import heappop
from heapq import heappushpop

import numpy as np
from scipy.spatial import cKDTree as KDTree
from itertools import takewhile


class KDTreeModel(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self._users = {}
        self._id_sequence = 0

    def rebuild_model(self):
        # This bookkeeping is very inefficient in terms of memory
        # but it helps make get-nearest-neighbors request faster
        self._fixed_order = list(self._users.items())
        self._user_ids = [key for key, data in self._fixed_order]
        locations = [(data['x'], data['y']) for i, data in self._fixed_order]

        self._locations = np.array(locations)
        self._model = KDTree(self._locations)

    def _filter_query_result(self, user_id, distances, indices, radius):
        # Drop the first candidate, it's the user_id himself
        rest = list(zip(distances, indices))[1:]
        # Keep only entries within the radius
        rest = list(takewhile(lambda pair: pair[0] < radius, rest))
        return [index for distance, index in rest]

    def get_nearest(self, user_id, k_neighbors, radius):
        if not self.is_present(user_id):
            return None

        k_neighbors = min(k_neighbors, len(self._users) - 1)

        user_data = self._users[user_id]
        user_location = np.array([user_data['x'], user_data['y']])

        distances, indices = self._model.query(user_location, k=k_neighbors+1)

        # If only one neighbor has been requested, `indices` will be an int64
        # (not iterable)
        if isinstance(indices, int):
            distances = [distances]
            indices = [indices]

        indices = self._filter_query_result(user_id, distances, indices, radius)

        # 0 -- user_id, the key of self._fixed_order items
        # 1 -- user_data, the value of self._fixed_order items
        return [self._fixed_order[index][1] for index in indices
                if self._fixed_order[index][0] != user_id]

    def get_nearest_naive(self, user_id, k_neighbors, radius):
        """
        This version is computationally inefficient. It is implemented to be
        a waterline for futher improvements.
        """
        needle_user_data = self._users[user_id]
        requested_user_location = np.array([needle_user_data['x'],
                                            needle_user_data['y']])

        indices = []
        for current_user_id, user_data in self._users.items():
            if current_user_id == user_id:
                continue

            current_user_location = np.array([user_data['x'], user_data['y']])
            distance = np.linalg.norm(requested_user_location - current_user_location)
            if distance >= radius:
                continue

            # Pythons' heapq is min-heap, so we negate the distance to turn
            # it into max-heap
            item = (-distance, current_user_id)
            if len(indices) < k_neighbors:
                heappush(indices, item)
            else:
                heappushpop(indices, item)

        # Sort candidates by distance (ascending)
        candidates = [(distance, self._users[index])
                      for distance, index in indices]
        candidates = sorted(candidates, key=lambda pair: -pair[0])
        return [user_data for distance, user_data in candidates]

    def is_present(self, user_id):
        return user_id in self._users

    def get_user(self, user_id):
        if not self.is_present(user_id):
            return None

        return self._users[user_id]

    def create_user(self, location_x, location_y, name, age, rebuild_model=True):
        user_id = self._id_sequence
        self._users[user_id] = {'x': location_x,
                                'y': location_y,
                                'name': name,
                                'age': age}
        self._id_sequence += 1
        if rebuild_model:
            self.rebuild_model()
        return user_id

    def delete_user(self, user_id):
        if not self.is_present(user_id):
            return None

        del self._users[user_id]
        self.rebuild_model()
        return user_id

    def update_user(self, user_id, location_x, location_y, name, age):
        if not self.is_present(user_id):
            self._users[user_id] = {}

        user = self._users[user_id]
        user['x'] = location_x
        user['y'] = location_y
        user['name'] = name
        user['age'] = age
        self._users[user_id] = user
        self.rebuild_model()
        return user_id
