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
* AIOHTTP
* React

Running apps
------------
The Python API is executed as follows:
~~~
    source ./venv/Scripts/activate
    adev runserver app --livereload
~~~
The server will be listening on http://localhost:8000/

To run the React front-end, execute this:
~~~
    cd ./web/app
    yarn start
~~~

Python environment
------------------
~~~
    git clone {this_repo}

    ## Install virtualenv and yarn
    sudo pip install virtualenv
    curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
    echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
    sudo apt update && sudo apt install yarn

    ## Create venv and install python dependencies
    virtualenv venv --python=python3
    cd ragnarok/
    source ./venv/Scripts/activate
    pip install -r requirements.txt
    
    ## Install node dependencies
    cd web/app/
    yarn install
~~~