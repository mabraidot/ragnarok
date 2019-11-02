RAGNARÖK
========
Automated brewing machine.

This project is based on the following hardware:
* Raspberry Pi 3
* Temperature sensors
* Water pumps
* Electrical water heaters
* Servo-assisted valves

On the software side:
* Python
* Flask
* React

Running apps
------------
The Python API is executed as follows:
~~~
    source ./venv/Scripts/activate
    flask run
~~~
The server will be listening on http://localhost:5000/

To run the React front-end, execute this:
~~~
    cd ./web/app
    yarn start
~~~

Python environment
------------------
~~~
    virtualenv venv --python=python3
    source ./venv/Scripts/activate
    git clone {this_repo}
~~~