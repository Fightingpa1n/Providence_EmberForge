import os
import shutil
import gdown

import debug as Debug

#=================================== PATHS ===================================#
ROAMING = os.getenv("APPDATA") #roaming directory
LOCAL = os.getenv("LOCALAPPDATA") #local directory

TEMP = os.path.join(ROAMING, ".providence_runstaller_temp") #temporary location for the files in the appdata folder

#=================================== TEMP ===================================#
def temp(): #check if the temp folder exists and if not create it
    if not os.path.exists(TEMP):
        try:
            os.mkdir(TEMP)
        except Exception as e:
            Debug.error_exit(f"An error occurred while creating the temp folder: {e}")

def temp_delete(): #delete the temp folder
    try:
        shutil.rmtree(TEMP, ignore_errors=True)
    except Exception as e:
        Debug.error(f"An error occurred while deleting the temp folder: {e}")

def temp_download(file_name, file_id): #download a file from google drive using the file id
    try:
        output = gdown.download(f"https://drive.google.com/uc?id={file_id}", os.path.join(TEMP, file_name), quiet=True)
        if output is None:
            raise Exception("Download failed or file is not found.")
    except Exception as e:
        raise Exception(f"An error occurred while downloading the file: {e}")

def temp_move(file_name, destination): #move a file from the temp folder to a destination
    try:
        file_name = os.path.join(TEMP, file_name) #make sure the file is in the temp folder
        if os.path.exists(file_name):
            shutil.move(file_name, destination)
        else:
            raise Exception("File not found")
    except Exception as e:
        raise Exception(f"An error occurred while moving the file: {e}")

def temp_remove(filename): #delete a file or directory
    try:
        filename = os.path.join(TEMP, filename) #make sure the file is in the temp folder
        if os.path.exists(filename):
            if os.path.isdir(filename):
                shutil.rmtree(filename, ignore_errors=True)
            else:
                os.remove(filename)
    except Exception as e:
        Debug.error(f"An error occurred while deleting the file: {e}")
