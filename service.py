"""
This service allows you to retrieve closest neighbors of a given user.
The following methods are supported:

    GET /
    Display this help message

    POST /user/?x=<float>&y=<float>&name=<str>&age=<int>
    Create new user

    PUT /user/<int>/?x=<float>&y=<float>&name=<str>&age=<int>
    Update information of a given user id

    DELETE /user/<int>
    Delete user by id

    GET /user/<int>
    Show information about user by id

    DELETE /user/
    Delete all users

    POST /generate?n=<int>
    Generate N random users (for testing purposes)
"""
from flask import Flask
from flask import Response
from flask import request
from flask import jsonify

from model import KDTreeModel
from test_model import generate_model


app = Flask(__name__)


query_model = KDTreeModel()


def make_status(status_code, message, result):
    return jsonify({
        'status_code': status_code,
        'message': message,
        'result': result
    })


@app.route('/user/<int:user_id>/neighbors')
def user_get_neighbors(user_id):
    radius = float(request.args.get('radius', 10.0))
    k_neighbors = int(request.args.get('k', 3))

    neighbors = query_model.get_nearest(user_id, k_neighbors, radius)
    if neighbors is None:
        return make_status(404, 'user not found', None)

    requested_user = query_model.get_user(user_id)
    return make_status(200, 'ok', {'requested_user': requested_user,
                                   'len': len(neighbors),
                                   'neighbors': neighbors})


@app.route('/user/', methods=['POST'])
def user_create():
    location_x = float(request.args.get('x', 0.0))
    location_y = float(request.args.get('y', 0.0))
    name = request.args.get('name', 'John')
    age = int(request.args.get('age', 20))

    user_id = query_model.create_user(location_x, location_y, name, age)
    return make_status(200, 'ok', {'user_id': user_id})


@app.route('/user/<int:user_id>', methods=['PUT'])
def user_update(user_id):
    location_x = float(request.args.get('x', 0.0))
    location_y = float(request.args.get('y', 0.0))
    name = request.args.get('name', 'John')
    age = int(request.args.get('age', 20))

    user_id = query_model.update_user(user_id, location_x, location_y, name, age)
    return make_status(200, 'ok', {'user_id': user_id})


@app.route('/user/<int:user_id>', methods=['DELETE'])
def user_delete(user_id):
    user_id = query_model.delete_user(user_id)
    if user_id is None:
        return make_status(404, 'user not found', None)

    return make_status(200, 'ok', {'user_id': user_id})


@app.route('/user/<int:user_id>')
def user_get(user_id):
    user_data = query_model.get_user(user_id)
    if user_data is None:
        return make_status(404, 'user not found', None)

    return make_status(200, 'ok', user_data)


@app.route('/user/', methods=['DELETE'])
def users_reset():
    query_model.reset()
    return make_status(200, 'ok', None)


@app.route('/generate', methods=['POST'])
def generate():
    n = int(request.args.get('n', 10))
    delta = generate_model(query_model, n)
    return make_status(200, 'ok', {'time_spent': delta})


@app.route('/')
def root():
    return Response(response=__doc__,
                    status=200,
                    mimetype='plain')
