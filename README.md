## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:zeeviiosub/advanced-system-design-project.git
    ...
    $ cd advanced-system-design-project/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [advanced-system-design-project] $ # you're good to go!
    ```

3. To check that everything is working as expected, run the tests:


    ``` sh
    $ pytest tests/
    ...
    ```

## Usage

TO RUN EVERYTHING ON THE SERVER SIDE:

```sh
$ run_pipeline.sh
```
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
  $ python -m parsers parse 'pose' 'snapshot.raw'
  ```
  
  Where `'snapshot.raw'` is a file containing raw data to be parsed. The result is printed to the standard output.
  
  
  It can also be invoked from the command line with a rabbitmq hostname. When invoked in this way, it reads messages from the queue tagged with the field name (e.g., `pose`), and sends the parsed data to the queue with a tag like `save_pose`.
  
  ```sh
  $ python -m parsers run-parser 'pose' '127.0.0.1'
  ```
  
  
 - `saver`

  This package provides the function `save`. It reads parsed data from the file (e.g., `pose.result`) and saves the data to the database.
  
  ```sh
  $ python -m saver save --database 'redis://localhost' 'pose' 'pose.result'
  ```
  
  This package also provides the function `run_saver`.
  `$queue_name` is of the form `save_field`, where `field` is either `user` or a field.
  
  ```sh
  $ python -m saver run-saver 'redis://localhost' 'rabbitmq://localhost' $queue_name 
  ```
    
  - `api`
  
  This is a program that runs the API server.
  
  ```sh
  $ python -m api run-server --host '127.0.0.1' --port 5000 --database '127.0.0.1'
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

To run the Web server: `python -m gui run-server --host 127.0.0.1 --port 8080 --api-host 127.0.0.1 --api-port 5000`.
