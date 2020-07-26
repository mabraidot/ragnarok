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
    source ./venv/bin/activate
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
    cd /home/pi/Documents/ragnarok/
    python main.py >/dev/null 2>&1 &
    P1=$!
    serve -s web/app/build/ >/dev/null 2>&1 &
    P2=$!
    wait $P1 $P2
~~~


Using DS18B20 temperature sensor
--------------------------------
Edit boot file:
~~~
    sudo nano /boot/config.txt
~~~
Uncomment or add the following line:
Reference (https://github.com/timofurrer/w1thermsensor)
~~~sh
    dtoverlay=w1–gpio
~~~

Config content
==============
Create the file /home/pi/Documents/ragnarok/app/config/config.cfg and place the next content,
then comment/uncomment appropriate section and adjust settings according environment:
~~~
[DEFAULT]
### PRODUCTION
# ENVIRONMENT=production
# SILENT=False
# SAVING_PARTIAL_PROCESS_INTERVAL=30
# RECIRCULATION_MASHTUN_FREQUENCY_TIME=180
# RECIRCULATION_MASHTUN_TIME=60
# RECIRCULATION_BOILKETTLE_FREQUENCY_TIME=300
# RECIRCULATION_BOILKETTLE_TIME=60
# NEXT_STEP_PRE_HEATING_TIME=15
# TEMP_LEFT_RACK_MASHTUN_REST=5
# BOIL_TEMPERATURE=110
# SPARGE_CYCLES_COUNT=6
# SPARGE_INFUSE_AMOUNT=4
# COOL_TIME=30
# PUMP_PRIMING_TIME=6
### DEVELOPMENT
ENVIRONMENT=development
SILENT=True
SAVING_PARTIAL_PROCESS_INTERVAL=4
RECIRCULATION_MASHTUN_FREQUENCY_TIME=6
RECIRCULATION_MASHTUN_TIME=5
RECIRCULATION_BOILKETTLE_FREQUENCY_TIME=10
RECIRCULATION_BOILKETTLE_TIME=2
NEXT_STEP_PRE_HEATING_TIME=0.5
TEMP_LEFT_RACK_MASHTUN_REST=5
BOIL_TEMPERATURE=110
SPARGE_CYCLES_COUNT=6
SPARGE_INFUSE_AMOUNT=2
COOL_TIME=1
PUMP_PRIMING_TIME=0

PUMP_READING_COUNT=8
ONE_LITER_WEIGHT=0.998
SAFE_WATER_LEVEL_FOR_HEATERS=3.2
SAFE_OVERHEAT_TEMPERATURE=10

LOG_NOTICE_LABEL=notice
LOG_NOTICE_PERSISTENT_LABEL=persistent_notice
LOG_ERROR_LABEL=error
LOG_ERROR_PERSISTENT_LABEL=persistent_error
COOL_TEMPERATURE=20
# PID AutoTune
PID_SET_POINT_TEMPERATURE=65
# Default: 100. Sets the output when stepping up/down.
PID_OUTSTEP=100
# Default: 100. Sets the max power output.
PID_MAXOUT=100
# Default: 30. How far back to look for min/max temps.
PID_LOOKBACK=30

[GENERAL_PINS]
SERVO_ENABLE=24
PUMP=23

[MASH_TUN_PINS]
HEATER=13
MAX_WATER_LEVEL=13
WATER_LEVEL_SENSOR_DT=26
WATER_LEVEL_SENSOR_SCK=6
WATER_LEVEL_SENSOR_REFERENCE_UNIT=-24.35
# SPI0: MOSI=10, MISO=9, SCLK=11, CE=22
TEMPERATURE_SENSOR_SPI_PORT=2
TEMPERATURE_SENSOR_ADDRESS=0319a27941a7
TEMPERATURE_SENSOR_OFFSET=3
PID_KP=37.609537321407885
PID_KI=0.3334124705293296
PID_KD=3.535353909840094

[BOIL_KETTLE_PINS]
HEATER=12
MAX_WATER_LEVEL=15
WATER_LEVEL_SENSOR_DT=25
WATER_LEVEL_SENSOR_SCK=5
WATER_LEVEL_SENSOR_REFERENCE_UNIT=-23.8
# SPI0: MOSI=10, MISO=9, SCLK=11, CE=27
TEMPERATURE_SENSOR_SPI_PORT=1
TEMPERATURE_SENSOR_ADDRESS=27
TEMPERATURE_SENSOR_OFFSET=0
PID_KP=50.065697262159894
PID_KI=0.58756202913738
PID_KD=3.555048826116045
~~~