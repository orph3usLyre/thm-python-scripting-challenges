## This script was written for the third THM scripting challenge: https://tryhackme.com/room/scripting
## It connects to a udp server, sends specific payloads to receive information from the server:
## It receives an aes-gcm key, iv (nonce), and a list of potential flags.
## It also takes in a sha256 hash value of the plaintext flag. 
## Then it grabs the ciphertext andd tag for each message, sent sequentially by the server, and attempts to decrypt them.
## Then, it compares the hash of the decrypted ciphertext with the hash initially sent by the server,
## and prints out the correct flag!

import socket
import os, sys
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import time

FORMAT = 'utf-8'

def send_and_receive(socket, message):
    message = bytes(message, FORMAT)
    sent = socket.sendto(message, server_address)
    data, server = socket.recvfrom(4096)
    # print('Received:\n {!r}'.format(data))
    return data

server_address = ('10.10.219.38', 4000)
payloads = ['hello', 'ready to receive more information', 'final']

# Beginning:
# Create a UDP socket and connect
print(f"Opening socket.")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
done = False
try:
    # Sending first two payloads and receiving data
    print("Getting first two messages")
    initial_data = b''
    for i in range(2):
        data = send_and_receive(sock, payloads[i])
        initial_data += data
        time.sleep(1)
    # getting hash to compare with
    hash = initial_data.split()[31].hex()
    nonce = b'secureivl337'
    key = b'thisisaverysecretkeyl337'
    count = 0
    print(f"Collecting flags")
    while not done:
        cipher_text = send_and_receive(sock, payloads[2])
        if (count >= 100) | (cipher_text == b"That won't work friend ;)"):
            break
        tag = send_and_receive(sock, payloads[2])
        complete_data = cipher_text + tag
        print(f"Checking flags at count: {count}", end=' ')
        aesgcm = AESGCM(key)
        associated_data = b''
        try:
            plain_text = aesgcm.decrypt(nonce, complete_data, associated_data)
            print(f"Decrypted message: {plain_text}.", end=' ')
        except Exception as ex:
            continue
        else:
            checksum = hashlib.sha256(plain_text).hexdigest()
            if checksum == hash:
                print(f"Hash matched. The flag is: {plain_text}")
                done = True
            else:
                print("Wrong hash.")
        finally:
            count += 1
            time.sleep(1)

except Exception as ex:
    print(ex)
finally:
    print(f'Finished. Closing socket.')
    sock.close()

