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

Start Ragnarök in kiosk mode
----------------------------
Set custom boot image and remove boot messages:
Edit the file:
~~~
    sudo nano /boot/cmdline.txt
~~~
With the following content:
~~~sh
    dwc_otg.lpm_enable=0 console=serial0,115200 console=tty3 root=PARTUUID=4afadf26-02 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles logo.nologo vt.global_cursor_default=0
~~~

Edit the file:
~~~
    sudo nano /usr/share/plymouth/themes/pix/pix.script
~~~
Comment out these lines and change splash image url
~~~sh
    #message_sprite = Sprite();
    #message_sprite.SetPosition(screen_width * 0.1, screen_height * 0.9, 10000);
~~~

Then overwrite splash image with your own:
~~~
    sudo cp /home/pi/Documents/ragnarok/web/app/src/background.png /usr/share/plymouth/themes/pix/splash.png
~~~

Edit autostart file:
~~~
    sudo cp /etc/xdg/lxsession/LXDE-pi/autostart /etc/xdg/lxsession/LXDE-pi/autostart.bk
    sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
~~~
With the following content:
~~~sh
    #@lxpanel --profile LXDE-pi
    #@pcmanfm --desktop --profile LXDE-pi
    #@xscreensaver -no-splash
    @unclutter -idle 0
    @xset s off
    @xset -dpms
    @xset s noblank
    @sed -i 's/"exited_cleanly": false/"exited_cleanly": true/' ~/.config/chromium-browser Default/Preferences
    @bash /home/pi/start.sh
    @chromium-browser --noerrdialogs --disable-infobars --kiosk http://localhost:5000/loading --incognito
~~~

Create the startup bash script:
~~~
    touch /home/pi/start.sh
~~~
With the following content:
~~~sh
    #!/bin/bash

    source /home/pi/Documents/ragnarok/venv/bin/activate
    serve -s /home/pi/Documents/ragnarok/web/app/build/ >/dev/null 2>&1 &
    P1=$!
    cd /home/pi/Documents/ragnarok/
    python main.py >/dev/null 2>&1 &
    P2=$!
    wait $P1 $P2
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