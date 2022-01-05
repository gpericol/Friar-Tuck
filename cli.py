import psutil
import subprocess
from data.config.config import *
from os import remove
from os.path import exists
import argparse
import json

def check_process_up():
    if not exists(CONFIG["path_pid"]):
        return False
    
    with open(CONFIG["path_pid"], 'r') as pid_file:
        pid = int(pid_file.read())

    # program crashed
    if not psutil.pid_exists(pid):
        remove(CONFIG["path_pid"])
        return False

    return True

def print_hardware(data):
    print(f"temperature: {data['temperature']}°C\nheater:{data['heater']}\ncooler: {data['cooler']}")


def check_status():
    if not check_process_up():
        print("[-] Friar Tuck is sleeping")
        return
    
    print("[+] Friar Tuck is running")
    with open(CONFIG["path_status"], 'r') as status_file:
        data = json.load(status_file)

        if data["type"] == "smart":
            print("mode: Smart")
            print(f'threshold: ±{data["threshold"]}°C')
            print(f'curve name: { data["curve_name"] }')
            if data["smart_mode"]:
                print("smart mode type: curve")
            else:
                print("smart mode type: ramp up")
            
            print(f'running time: { data["running_time"]}h')
            
        else:
            print("mode: Static")
            print(f'threshold: ±{data["threshold"]}°C')
            print(f'targert temperature: ±{data["target_temperature"]}°C')

        print_hardware(data["hardware_status"])


def list_curves():
    print("Curves List")
    print("-----------")
    with open(CONFIG["path_curves_list"], 'r') as curves_list_file:
        data = json.load(curves_list_file)

        for curve in data["curves"]:
            print(f'id: {curve["id"]}\nname: {curve["name"]}\ndescription: {curve["description"]}\n')

def terminate():
    if not check_process_up():
        print("[-] Friar Tuck already is sleeping")
        return

    remove(CONFIG["path_pid"])
    print("[-] Friar Tuck was put to sleep")
    
def launch_smart(curve_id, threshold, delay=0):
    if check_process_up():
        print("[-] Friar Tuck is already working")
        return

    with open(CONFIG["path_curves_list"], 'r') as curves_list_file:
        data = json.load(curves_list_file)
        if curve_id not in range(0, len(data["curves"])):
            print("Friar Tuck doesn't know the curve you are looking for")
            return

    exec_params = ['python', 'friar_tuck.py','--curve', str(curve_id), str(threshold)]
    
    if delay > 0:
        exec_params = ['python', 'friar_tuck.py','--delayed_curve', str(curve_id), str(threshold), str(delay)]
    else:
        exec_params = ['python', 'friar_tuck.py','--curve', str(curve_id), str(threshold)]

    subprocess.Popen(exec_params, stdout=subprocess.PIPE, shell=False)
    print("[+] Friar Tuck is at work")

def launch_static(temperature, threshold):
    if check_process_up():
        print("[-] Friar Tuck is already working")
        return

    subprocess.Popen(['python', 'friar_tuck.py','--static', str(temperature), str(threshold)], stdout=subprocess.PIPE, shell=False)
    print("[+] Friar Tuck is at work")


def logo():
    logo = '''
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
    '''
    print(logo)

def main():
    parser = argparse.ArgumentParser(description='Friar Tuck CLI')
    parser.add_argument('-s', '--status', action='store_true', help='Check status of the thermostat')
    parser.add_argument('-l', '--list', action='store_true', help='List available curves for smart thermostat')
    parser.add_argument('-t', '--terminate', action='store_true', help='Stop thermostat')
    parser.add_argument('-sm', '--smart', type=int, nargs=2, metavar=('curve_id', 'threshold'), help='Start thermostat in smart mode with <curve_id> curve and <threshold> threshold')
    parser.add_argument('-dsm', '--delayed_smart', type=int, nargs=3, metavar=('curve_id', 'threshold', 'delay'), help='Start thermostat in smart mode with <curve_id> curve, <threshold> threshold and <delay> delay ')
    parser.add_argument('-st', '--static', type=int, nargs=2, metavar=('temperature', 'threshold'), help='Start thermostat in static mode with <temperature> temperature and <threshold> threshold')

    args = parser.parse_args()

    if args.status:
        check_status()
    elif args.list:
        list_curves()
    elif args.terminate:
        terminate()
    elif args.smart:
        launch_smart(args.smart[0], args.smart[1])
    elif args.delayed_smart:
        launch_smart(args.delayed_smart[0], args.delayed_smart[1], args.delayed_smart[2])
    elif args.static:
        launch_static(args.static[0], args.static[1])
    else:
        logo()
        parser.print_help()

if __name__ == "__main__":
    main()