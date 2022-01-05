import json
from os import walk,remove,getpid
from os.path import join, exists
import time
import argparse

from data.config.config import *
from curve.curve import Curve
from hardware.fake_hardware import FakeHardware
from thermostat.static_thermostat import StaticThermostat
from thermostat.smart_thermostat import SmartThermostat

def load_curves(path):
    curves = []
    file_names = next(walk(path), (None, None, []))[2]

    for file_name in file_names:
        with open(join(path, file_name)) as curve_file:
            curves.append(Curve(json.load(curve_file)))

    return curves

def index_curves(curves):
    result = {
        "curves": []
    }

    for idx, curve in enumerate(curves):
        result["curves"].append({
            "id": idx,
            "name": curve.get_name(),
            "description": curve.get_description()
        })

    return result

def clean_up_processes():
    if exists(CONFIG["path_pid"]):
        remove(CONFIG["path_pid"])
        time.sleep(3)

def main():
    curves = load_curves(CONFIG["path_curves"])

    parser = argparse.ArgumentParser(description='Server Program')
    parser.add_argument('-s', '--static', type=int, nargs=2, metavar=('temperature', 'threshold'), help='Start thermostat in static mode with <temperature> temperature and <threshold> threshold')
    parser.add_argument('-c', '--curve', type=int, nargs=2, metavar=('curve_id', 'threshold'), help='Start thermostat in smart mode with <curve_id> curve and <threshold> threshold')
    parser.add_argument('-dc', '--delayed_curve', type=int, nargs=3, metavar=('curve_id', 'threshold', 'delay'), help='Start thermostat in smart mode with delay')
    parser.add_argument('-u', '--update', action='store_true', help='Update curves index')
    
    args = parser.parse_args()

    if args.update:
        with open(CONFIG["path_curves_list"], 'w') as list_file:
            json.dump(index_curves(curves), list_file)
        print("Curves index updated")
        exit()

    if args.curve and args.curve[0] not in range(0, len(curves)):
        print(f"error: wrong curve number")
        exit()

    if args.delayed_curve and args.delayed_curve[0] not in range(0, len(curves)):
        print(f"error: wrong curve number")
        exit()

    hardware = FakeHardware()
    
    if args.static:
        thermostat = StaticThermostat(hardware, args.static[1], args.static[0])
    elif args.curve:
        thermostat = SmartThermostat(hardware, args.curve[1], curves[args.curve[0]])
    elif args.delayed_curve:
        thermostat = SmartThermostat(hardware, args.delayed_curve[1], curves[args.delayed_curve[0]], args.delayed_curve[2])
    else:
        parser.print_help()
        exit()

    # cleanup other instances of same project
    clean_up_processes()

    #store pid
    with open(CONFIG["path_pid"], 'w') as pid_file:
        pid_file.write(str(getpid()))

    while exists(CONFIG["path_pid"]):
        with open(CONFIG["path_status"], 'w') as status_file:
            json.dump(thermostat.run(), status_file)
        time.sleep(2)

    thermostat.turn_off()
    remove(CONFIG["path_status"])

if __name__ == "__main__":
    main()