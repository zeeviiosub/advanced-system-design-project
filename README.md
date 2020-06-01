## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:zeeviiosub/advanced-system-design-project.git
    ...
    $ cd foobar/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [advanced-system-design-project] $ # you're good to go!
    ```

3. To check that everything is working as expected, run the tests:


    ```sh
    $ pytest tests/
    ...
    ```

## Usage

The following packages are provided:

- `client`

    This package provides the function `upload_sample`.

    ```pycon
    >>> from client import upload_sample
    >>> upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz')
    ```
    
    It can also be invoked in the command line.
    
    ```sh
    $ python -m client upload-sample --host '127.0.0.1' --port 8000 'snapshot.mind.gz'
    ```

- `server`

  This package provides the function `run_server`.
    ```pycon
    >>> from server import run_server
    >>> run_server(host='127.0.0.1', port=8000, publish=print_message)
    ```
  It can also be invoked in the command line.
    ```sh
    $ python -m server run-server --host '127.0.0.1' --port 8000 '127.0.0.1'
    ```
 
 - `parsers`

  This package provides the function `run_parser` (the last argument is the queue address).
  In addition for parsers for fields, there is a parser for `user` (the user data).
    ```pycon
    >>> from parsers import run_parser
    >>> run_parser('pose', '127.0.0.1')
    ```
  It can also be invoked in the command line.
    ```sh
    $ python -m parsers run-parser 'pose' '127.0.0.1'
    ```
  
  
 - `saver`

  This package provides the function `save`.
    ```sh
    $ python -m saver save --database 'redis://localhost' 'pose' $data_as_json_string
    ```
  This package also provides the function `run_saver`.
  `$queue_name` is of the form `save_field`, where `field` is either `user` or a field.
    ```sh
    $ python -m saver run-saver --database 'redis://localhost' --queue_address 'localhost' $queue_name 
    ```
    
  - `api`
  
  This is a program that runs on the API server (127.0.0.1:9000).
    ```sh
    $ python api.py
    ```
  
  The API includes the following:
  
  `GET /users`
  
  Returns the list of all the supported users, including their IDs and names only.
  
  `GET /users/user-id`
  
  Returns the specified user's details: ID, name, birthday and gender.
  
  `GET /users/user-id/snapshots`
  
  Returns the list of the specified user's snapshot IDs and datetimes only.
  
  `GET /users/user-id/snapshots/snapshot-id`
  
  Returns the specified snapshot's details: ID, datetime, and the available results' names only (e.g. `pose`).
  
  `GET /users/user-id/snapshots/snapshot-id/result-name`
  
  Returns the specified snapshot's result.
  
  The information is returned as a string representing a JSon object. One field is `error` (containing the error message), and the other field is `user`, `user`, `snapshots`, `snapshot` or `result`, respectively, containing the data requested.
  
  - `apicli`
  
  The API can be invoked through the CLI.
  ```sh
  $ python -m apicli get-users
…
$ python -m apicli get-user 1
…
$ python -m apicli get-snapshots 1
…
$ python -m apicli get-snapshot 1 2
…
$ python -m apicli get-result 1 2 'pose'
…
```

- The Web application.

To run the Web server: `python web/app.py`.

The main page URL is `http://127.0.0.1:7000/`.
