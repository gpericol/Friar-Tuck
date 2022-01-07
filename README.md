# Friar Tuck

An intelligent thermostat for beer fermentation.

- it works as simple thermostat
- it works as a smart thermostat that follow a configurable curve
- there is a CLI management tool
- there is a Telegram bot management tool 

Designed to run on Raspberry Pi 3 Model B+
```
   ________)                  ______)       
  (, /         ,             (, /        /) 
    /___, __     _   __        /      _ (/_ 
 ) /     / (__(_(_(_/ (_    ) /  (_(_(__/(__
(_/                        (_/              
                                           
            ,-----.  .-.-.-.-.-.-..-..-.
           #,-. ,-.# '.  Damn buggers!  )    
          () a   e ()  ).'^^^^^^^^^^^^^'    
          (   (_)   )  .    
          #\_  -  _/# . *.
        ,'   `"""`    0oOo
      ,'      \X/     ||||)o
     /         X      |||| \ 
    /          v     \`""' /
```

#### Designed and built with all the Love❤️ in the World🌍 by Gianluca Pericoli

## Hardware
- Raspberry Pi 3 Model B+
- DS18B20 sensor -50 - + 125
- 2 Channel DC 5V Relay Module with Optocoupler Low Level Trigger Expansion Board for Arduino R3 MEGA 2560 1280 DSP ARM PIC AVR

## Mount
- DS18B20 sensor -50 - + 125 is connected to GPIO pin 7
- Relay Module is connected on pins 16 and 18

## Configuration
copy file
```
data/config/edit_me_config.py
```
to 
```
data/config/config.py
```

### Installation
#### Python libraries
```
$ pip install -r requirements.txt
```

#### Configure DS18B20
``` 
$ sudo nano /boot/config.txt
```
and add
```
dtoverlay=w1-gpio
```

### Pin configuration
if you want to change Cooler and Heater relays just change:
```
"in_heater": 16,
"in_cooler": 18
```

### Telegram configuration (if you want to use Telegram bot feature)

Modify telegram_users adding telegram ID (9 digits) on the list and write on the token the one provided by BotFather
```
"telegram_users": [],
"telegram_token": "",
```

### Curves
You can find a bunch of generic curves on
```
data/curves/
```
e.g.
```json
{
    "name": "Lager",
    "description": "A Lager Beer",
    "curve": [
        {
            "hour": 0,
            "temperature": 10
        },
        {
            "hour": 24,
            "temperature": 12
        },
        {
            "hour": 144,
            "temperature": 12
        },
        {
            "hour": 168,
            "temperature": 20
        },
        {
            "hour": 216,
            "temperature": 20
        },
        {
            "hour": 240,
            "temperature": 0
        }
    ]
}
```
when you change them or you add stuff just launch:
```
$ python friar_tuck.py --update
```

## How does it work
You can use it on CLI mode and as Telegram Bot (both of them):

```
$ python cli.py


   ________)                  ______)       
  (, /         ,             (, /        /) 
    /___, __     _   __        /      _ (/_ 
 ) /     / (__(_(_(_/ (_    ) /  (_(_(__/(__
(_/                        (_/
                                            
            ,-----.  .-.-.-.-.-.-..-..-.
           #,-. ,-.# '.  Damn buggers!  )
          () a   e ()  ).'^^^^^^^^^^^^^'
          (   (_)   )  .
          #\_  -  _/# . *.
        ,'   `"""`    0oOo
      ,'      \X/     ||||)o
     /         X      |||| \
    /          v     \`""' /

usage: cli.py [-h] [-s] [-l] [-t] [-sm curve_id threshold] [-dsm curve_id threshold delay] [-st temperature threshold]

Friar Tuck CLI

optional arguments:
  -h, --help            show this help message and exit
  -s, --status          Check status of the thermostat
  -l, --list            List available curves for smart thermostat
  -t, --terminate       Stop thermostat
  -sm curve_id threshold, --smart curve_id threshold
                        Start thermostat in smart mode with <curve_id> curve and <threshold> threshold
  -dsm curve_id threshold delay, --delayed_smart curve_id threshold delay
                        Start thermostat in smart mode with <curve_id> curve, <threshold> threshold and <delay> delay
  -st temperature threshold, --static temperature threshold
                        Start thermostat in static mode with <temperature> temperature and <threshold> threshold
```

and 

```
$ python telegram_bot.py
```

add it to a channel, set on config your ID and have fun

```
*Commands*
/status - check status
/terminate - stop thermostat
/list - available curves
/smart <curve id> <threshold>
/dsmart <curve id> <threshold> <delay>
/static <temperature> <threshold>
```

## LICENCE

This program is free software; you can redistribute it and/or modify it under the terms of the [GNU General Public License](https://www.gnu.org/licenses/gpl-3.0.html) as published by the Free Software Foundation; either version 3 of the License, or(at your option) any later version.