# Bird song recordings

- Consumes the API located in https://xeno-canto.org/api/2/recordings?query=cnt:ecuador

- Code contains functions to fetch the recordings data from the API, filter them by recording length and count how many of each recording type there are

- Code includes unit tests in `pytest`

# Installation

- Pull the code from this repo

- You can install dependencies with `pipenv` or `pip`

    -  With `pipenv`
        ```
        pipenv install
        ```

    - With `pip`
        ```
        pip install -r requirements.txt
        ```

- To run unit tests, first install dependencies and the run
    ```
    pytest . -v
    ```
