RAGNARÖK
========
Automated brewing machine.
This is yet a Work In Progress!

This project is intended for a small 480 x 800 px display and based on the following hardware:
* Raspberry Pi 3
* Touch display 7" for RPi3
* Temperature sensors
* Water pump
* Electrical water heaters
* Servo-assisted valves
* Scale sensors for water level sensing

On the software side:
* Python
* AIOHTTP
* React

Running apps
------------
The Python API is executed as follows:
~~~
    source ./venv/Scripts/activate
    adev runserver . --livereload
~~~
or for production:
~~~
    source ./venv/Scripts/activate
    python main.py
~~~
The server will be listening on http://localhost:8000/

To run the React front-end, execute this:
~~~
    cd ./web/app
    yarn start
~~~
or for production:
~~~
    cd ./web/app
    yarn build
    serve -s build/
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
    cd ragnarok/
    virtualenv venv --python=python3
    source ./venv/Scripts/activate
    pip install -r requirements.txt
    
    ## Install node dependencies
    cd web/app/
    yarn install
~~~

Text-To-Speech
--------------
Install gTTS:
~~~
    pip install gTTS
~~~

Generate every needed audible message into /app/sounds/ folder:
~~~
    gtts-cli 'The ragnarok is coming in 3, 2, 1' --output app/sounds/test.mp3
~~~