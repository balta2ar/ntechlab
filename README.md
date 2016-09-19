# NTechLab homework for Python developer candidates

## Problem

> Напишите REST-сервис для поиска соседей. Основная функция - сервис должен
> позволить запросить K ближайших соседей пользователя N в радиусе M километров.
> Помимо этого сервис должен позволять выполнять простейшие CRUD-действия над
> пользователями - создавать пользователя с координатами (2D, на плоскости,
> сфере или геоиде - не суть), модифицировать информацию о нём (координаты,
> какое-нибудь описание, по желанию), удалять. У вас один миллион пользователей
> и один вечер.

## Installation

It's recommended that you use [conda](http://conda.pydata.org/miniconda.html)
to set up your Python environment.

``` bash
git clone https://github.com/balta2ar/ntechlab
cd ntechlab

conda create -n ntechlab python=3.5
conda install --file=requirements.txt
source activate ntechlab
```

## Running

``` bash
$ make unittest
python -m unittest test_model
...Generating 1000 items
Done generating 1000 items (0.0s)
........Generating 100 items
Done generating 100 items (0.0s)
Measuring...

100 items: get_nearest takes 0.07020s for 1000 runs
Generating 1000 items
Done generating 1000 items (0.0s)
Measuring...

1000 items: get_nearest takes 0.07101s for 1000 runs
Generating 10000 items
Done generating 10000 items (0.1s)
Measuring...

10000 items: get_nearest takes 0.07246s for 1000 runs
Generating 100000 items
Done generating 100000 items (1.2s)
Measuring...

100000 items: get_nearest takes 0.07200s for 1000 runs
Generating 1000000 items
Done generating 1000000 items (12.9s)
Measuring...

1000000 items: get_nearest takes 0.07259s for 1000 runs
.
----------------------------------------------------------------------
Ran 12 tests in 26.710s

OK

$ make run
FLASK_APP=service.py flask run
 * Serving Flask app "service"
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Now run in a separate terminal shell:

``` bash
$ make test

+ SERVICE=localhost:5000
+ OPTIONS=-v
+ http -v GET localhost:5000/
GET / HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:5000
User-Agent: HTTPie/0.9.6



HTTP/1.0 200 OK
Content-Length: 514
Content-Type: plain
Date: Mon, 19 Sep 2016 19:08:11 GMT
Server: Werkzeug/0.11.11 Python/3.5.2


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


+ http -v DELETE localhost:5000/user/
DELETE /user/ HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 0
Host: localhost:5000
User-Agent: HTTPie/0.9.6



HTTP/1.0 200 OK
Content-Length: 64
Content-Type: application/json
Date: Mon, 19 Sep 2016 19:08:11 GMT
Server: Werkzeug/0.11.11 Python/3.5.2

{
    "message": "ok",
    "result": null,
    "status_code": 200
}

+ http -v POST 'localhost:5000/user/?x=1000&y=3&name=Mark&age=30'
POST /user/?x=1000&y=3&name=Mark&age=30 HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 0
Host: localhost:5000
User-Agent: HTTPie/0.9.6



HTTP/1.0 200 OK
Content-Length: 82
Content-Type: application/json
Date: Mon, 19 Sep 2016 19:08:12 GMT
Server: Werkzeug/0.11.11 Python/3.5.2

{
    "message": "ok",
    "result": {
        "user_id": 0
    },
    "status_code": 200
}

+ http -v POST 'localhost:5000/user/?x=2000&y=3&name=Victor&age=33'
POST /user/?x=2000&y=3&name=Victor&age=33 HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 0
Host: localhost:5000
User-Agent: HTTPie/0.9.6



HTTP/1.0 200 OK
Content-Length: 82
Content-Type: application/json
Date: Mon, 19 Sep 2016 19:08:12 GMT
Server: Werkzeug/0.11.11 Python/3.5.2

{
    "message": "ok",
    "result": {
        "user_id": 1
    },
    "status_code": 200
}

+ http -v POST 'localhost:5000/user/?x=3000&y=3&name=Mary&age=35'
POST /user/?x=3000&y=3&name=Mary&age=35 HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 0
Host: localhost:5000
User-Agent: HTTPie/0.9.6



HTTP/1.0 200 OK
Content-Length: 82
Content-Type: application/json
Date: Mon, 19 Sep 2016 19:08:13 GMT
Server: Werkzeug/0.11.11 Python/3.5.2

{
    "message": "ok",
    "result": {
        "user_id": 2
    },
    "status_code": 200
}

+ http -v POST 'localhost:5000/user/?x=4000&y=3&name=Elena&age=36'
POST /user/?x=4000&y=3&name=Elena&age=36 HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 0
Host: localhost:5000
User-Agent: HTTPie/0.9.6



HTTP/1.0 200 OK
Content-Length: 82
Content-Type: application/json
Date: Mon, 19 Sep 2016 19:08:13 GMT
Server: Werkzeug/0.11.11 Python/3.5.2

{
    "message": "ok",
    "result": {
        "user_id": 3
    },
    "status_code": 200
}

+ http -v POST 'localhost:5000/user/?x=5000&y=3&name=Sam&age=37'
POST /user/?x=5000&y=3&name=Sam&age=37 HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 0
Host: localhost:5000
User-Agent: HTTPie/0.9.6



HTTP/1.0 200 OK
Content-Length: 82
Content-Type: application/json
Date: Mon, 19 Sep 2016 19:08:14 GMT
Server: Werkzeug/0.11.11 Python/3.5.2

{
    "message": "ok",
    "result": {
        "user_id": 4
    },
    "status_code": 200
}

+ http -v GET 'localhost:5000/user/0/neighbors?k=2&radius=10000'
GET /user/0/neighbors?k=2&radius=10000 HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:5000
User-Agent: HTTPie/0.9.6



HTTP/1.0 200 OK
Content-Length: 417
Content-Type: application/json
Date: Mon, 19 Sep 2016 19:08:14 GMT
Server: Werkzeug/0.11.11 Python/3.5.2

{
    "message": "ok",
    "result": {
        "len": 2,
        "neighbors": [
            {
                "age": 33,
                "name": "Victor",
                "x": 2000.0,
                "y": 3.0
            },
            {
                "age": 35,
                "name": "Mary",
                "x": 3000.0,
                "y": 3.0
            }
        ],
        "requested_user": {
            "age": 30,
            "name": "Mark",
            "x": 1000.0,
            "y": 3.0
        }
    },
    "status_code": 200
}

+ http -v GET 'localhost:5000/user/0/neighbors?k=10&radius=2500'
GET /user/0/neighbors?k=10&radius=2500 HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:5000
User-Agent: HTTPie/0.9.6



HTTP/1.0 200 OK
Content-Length: 417
Content-Type: application/json
Date: Mon, 19 Sep 2016 19:08:15 GMT
Server: Werkzeug/0.11.11 Python/3.5.2

{
    "message": "ok",
    "result": {
        "len": 2,
        "neighbors": [
            {
                "age": 33,
                "name": "Victor",
                "x": 2000.0,
                "y": 3.0
            },
            {
                "age": 35,
                "name": "Mary",
                "x": 3000.0,
                "y": 3.0
            }
        ],
        "requested_user": {
            "age": 30,
            "name": "Mark",
            "x": 1000.0,
            "y": 3.0
        }
    },
    "status_code": 200
}

+ http -v DELETE localhost:5000/user/4
DELETE /user/4 HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 0
Host: localhost:5000
User-Agent: HTTPie/0.9.6



HTTP/1.0 200 OK
Content-Length: 82
Content-Type: application/json
Date: Mon, 19 Sep 2016 19:08:15 GMT
Server: Werkzeug/0.11.11 Python/3.5.2

{
    "message": "ok",
    "result": {
        "user_id": 4
    },
    "status_code": 200
}

+ http -v DELETE localhost:5000/user/4
DELETE /user/4 HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 0
Host: localhost:5000
User-Agent: HTTPie/0.9.6



HTTP/1.0 200 OK
Content-Length: 76
Content-Type: application/json
Date: Mon, 19 Sep 2016 19:08:15 GMT
Server: Werkzeug/0.11.11 Python/3.5.2

{
    "message": "user not found",
    "result": null,
    "status_code": 404
}

+ http -v GET localhost:5000/user/1
GET /user/1 HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:5000
User-Agent: HTTPie/0.9.6



HTTP/1.0 200 OK
Content-Length: 135
Content-Type: application/json
Date: Mon, 19 Sep 2016 19:08:16 GMT
Server: Werkzeug/0.11.11 Python/3.5.2

{
    "message": "ok",
    "result": {
        "age": 33,
        "name": "Victor",
        "x": 2000.0,
        "y": 3.0
    },
    "status_code": 200
}

+ http -v PUT 'localhost:5000/user/1?x=7000&y=3&name=Brad&age=10'
PUT /user/1?x=7000&y=3&name=Brad&age=10 HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 0
Host: localhost:5000
User-Agent: HTTPie/0.9.6



HTTP/1.0 200 OK
Content-Length: 82
Content-Type: application/json
Date: Mon, 19 Sep 2016 19:08:16 GMT
Server: Werkzeug/0.11.11 Python/3.5.2

{
    "message": "ok",
    "result": {
        "user_id": 1
    },
    "status_code": 200
}

+ http -v GET localhost:5000/user/1
GET /user/1 HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:5000
User-Agent: HTTPie/0.9.6



HTTP/1.0 200 OK
Content-Length: 133
Content-Type: application/json
Date: Mon, 19 Sep 2016 19:08:17 GMT
Server: Werkzeug/0.11.11 Python/3.5.2

{
    "message": "ok",
    "result": {
        "age": 10,
        "name": "Brad",
        "x": 7000.0,
        "y": 3.0
    },
    "status_code": 200
}

+ http -v POST 'localhost:5000/generate?n=1000'
POST /generate?n=1000 HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 0
Host: localhost:5000
User-Agent: HTTPie/0.9.6



HTTP/1.0 200 OK
Content-Length: 104
Content-Type: application/json
Date: Mon, 19 Sep 2016 19:08:17 GMT
Server: Werkzeug/0.11.11 Python/3.5.2

{
    "message": "ok",
    "result": {
        "time_spent": 0.011723995208740234
    },
    "status_code": 200
}

+ http -v GET 'localhost:5000/user/0/neighbors?k=2&radius=5000'
GET /user/0/neighbors?k=2&radius=5000 HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:5000
User-Agent: HTTPie/0.9.6



HTTP/1.0 200 OK
Content-Length: 443
Content-Type: application/json
Date: Mon, 19 Sep 2016 19:08:18 GMT
Server: Werkzeug/0.11.11 Python/3.5.2

{
    "message": "ok",
    "result": {
        "len": 2,
        "neighbors": [
            {
                "age": 35,
                "name": "Mary",
                "x": 3000.0,
                "y": 3.0
            },
            {
                "age": 88,
                "name": "ztnCU",
                "x": 424.39365574842293,
                "y": 2188.9000472940843
            }
        ],
        "requested_user": {
            "age": 30,
            "name": "Mark",
            "x": 1000.0,
            "y": 3.0
        }
    },
    "status_code": 200
}
```
