import os
import sys
import ctypes
import time
import subprocess

#COLORS
COLOR_DEFAULT = "\033[0m" #default
COLOR_ERROR = "\033[91m" #red
COLOR_WARNING = "\033[93m" #yellow
COLOR_SUCCESS = "\033[92m" #green
COLOR_INFO = "\033[94m" #blue
COLOR_MESSAGE = "\033[97m" #white
COLOR_PROMPT = "\033[95m" #purple

#DELAYS
DELAY_ERROR = 1 #how long to display an error message before continuing
DELAY_WARNING = 0.5 #how long to display a warning message before continuing
DELAY_INFO = 0.8 #how long to display an info message before continuing
DELAY_SUCCESS = 0.5 #how long to display a success message before continuing
DELAY_MESSAGE = 1 #how long to display a message before continuing

DELAY_EXIT = 1 #how long to wait before exiting

def _color(message, color):
    return f"{color}{message}{COLOR_DEFAULT}"

#=================================== EXIT FUNCTIONS ===================================#
def error_exit(error_msg=""): #exit the program with an error
    if error_msg != "":
        print(_color(error_msg, COLOR_ERROR))
    else:
        print(_color("We encountered an unexpected error.", COLOR_ERROR))
        time.sleep(DELAY_ERROR)
    input(_color("Press enter to exit", COLOR_PROMPT))
    sys.exit(1)

def exit(): #exit the programs
    time.sleep(DELAY_EXIT)
    sys.exit(0)

def wait_exit(): #wait for the user to press enter before exiting
    input(_color("Press enter to exit", COLOR_PROMPT))
    sys.exit(0)

#=================================== PRINT FUNCTIONS ===================================#
def error(message=""): #print an error message
    print(_color(message, COLOR_ERROR))
    time.sleep(DELAY_ERROR)

def warning(message=""): #print a warning message
    print(_color(message, COLOR_WARNING))
    time.sleep(DELAY_WARNING)

def success(message=""): #print a success message
    print(_color(message, COLOR_SUCCESS))
    time.sleep(DELAY_SUCCESS)

def info(message=""): #print an info message
    print(_color(message, COLOR_INFO))
    time.sleep(DELAY_INFO)

def message(message=""): #print a message
    #messages will delete text before and after, so it's easier to read (deleting in this case means to scroll down so the message is at the top so it looks like it's the only message)
    os.system("cls")
    print(_color(message, COLOR_MESSAGE))
    time.sleep(DELAY_MESSAGE)
    os.system("cls")

def prompt(message="", default=""): #prompt the user for input
    value = input(_color(f"{message} (default: {default}): ", COLOR_PROMPT))
    if value == "":
        value = default
    return value

#=================================== ADMIN ===================================#
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        warning("there was an Error with checking for admin rights, continuing without admin rights")
        return False
