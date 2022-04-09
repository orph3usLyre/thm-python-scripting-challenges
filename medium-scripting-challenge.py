# https://realpython.com/python-sockets/
import socket
import requests
import time

# variables:
IP = "10.10.28.45"
PORT = 3010
number = 0
request = f"GET / HTTP/1.1\r\nHost:{IP}\r\n\r\n"


def get_port_webpage(IP, port):
    webtext = requests.get(url = f'http://{IP}:{port}').text
    next_port = webtext.split('"http://"+window.location.hostname+":')[1].split('"</script>')[0]
    return next_port
    

def connect_and_get_info(IP, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, int(port)))
    s.send(request.encode())  
    data = s.recv(1024).decode('utf-8')
    s.close()
    # print(f"Received {data!r}")
    return data


def calculate(number, opper, val):
    if opper == 'add':
        number = number + val
    elif opper == 'minus':
        number = number - val 
    elif opper == 'multiply':
        number = number * val
    elif opper == 'divide':
        number = number / val
    else:
        print("Did not receive valid opperator.")
        return 0
    return number



# Beginning:
print("Starting script...")
begun = False
while not begun:
    next_port = get_port_webpage(IP, PORT)
    if next_port == '1337':
        print(f"\nLoop has started. Next port is {next_port}")
        begun = True
        global done 
        done = False
    else:
        print(f"Waiting for port 1337. Current port is {next_port}. Refreshing...", end='\r')
        time.sleep(1)

while not done:
    try:
        info_raw = connect_and_get_info(IP, next_port)
        if not info_raw:
            continue
        info_split = info_raw.split()
        print(f"Successfully received data from port {next_port}...", end=' ')
        next_port = info_split[-1]
        if (next_port == 'STOP') | (next_port == '9765'):
            done = True
            print(f"Received STOP or reached port 9765. The final number is {number}.")
        next_port = info_split[-1]
        val = float(info_split[-2])
        opper = info_split[-3]
        print(f"The opper is: {opper}. The val is: {val}.")
        number = calculate(number, opper, val)
        print(f"Next port is {next_port}.", end=' ')
        print(f"The value of number is now {number}")
        list_of_lists.append(info_split)

    except ValueError as v:
        print(f"{v}. Full info_split is: {info_split}")
        print("Trying to reconnect...", end="\r")
        next_port = get_port_webpage(IP, PORT)
        continue
    except IndexError as i:
        print(f"{i}. Full data is: {info_raw}")
        continue
    except ConnectionRefusedError as e:
        print(f"{e}. Waiting 1 second...", end="\r")
        time.sleep(1)
        continue

print("\n")
print(f"Program has finished. Final number is {number}.")

