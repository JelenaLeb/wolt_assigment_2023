# Wolt Summer 2023 Engineering Internships

Delivery `Fee Calculator` for [Wolt Engineering Internships](https://github.com/woltapp/engineering-summer-intern-2023) implemented using Python, minimal version 3.9. It calculates a delivery fee based on the cart value, the number of items in the cart, the time of the order, and the delivery distance.

API implementation is done using [FastAPI](https://fastapi.tiangolo.com/) framework. 

For Unit tests was used [Pytest](https://docs.pytest.org/en/7.2.x/) framework.

## Getting started

_(Optional)_ It's recommened to use [virtual enviroment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/), as it allows to avoid installing Python packages globally which could break system tools or other projects.

```
$ python3 -m venv .venv/
$ source .venv/bin/activate
```

1. Install project dependenceies:

    ```
    $ make install
    ```
    Development dependencies are stored in separated file for convenience.

1. To consume Delivery Fee Calculator API  it is required to start a server, using following command:

    ```
    $ make server
    ```

    or trigger it manually:

    ```
    $ uvicorn --host 127.0.0.1 --port 9876 --reload src.api:app
    ```

1. Make a sample request in **new** terminal window (do not forget about virtual enviroment):

    ```
    $ make request
    ```

    or trigger it manually:

    ```
    $ curl -X POST http://127.0.0.1:9876/fee -H 'content-type: application/json' -d '{"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2021-10-12T13:00:00Z"}'

    {"delivery_fee":710}
    ```

## Development

Run unit tests using one of the following commands:

```
$ make test
$ make coverage
```
