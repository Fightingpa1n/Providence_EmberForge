import os
import gdown
import requests
import subprocess
import zipfile
import time
import shutil

import main as M
import debug as D
import check as C

def _check_using_version(program):
    try:
        params = (program.split("_") if "_" in program else [program]) + ["--version"]
        subprocess.run(params, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False




def _check_drive_url(url): #check if the url is valid
    #first we check if the url has the correct format.
    parameters = url.split("?")[1] #split the url at the question mark to get the variables
    if (not url.startswith("https://drive.google.com/uc")) or ("&" in parameters or not parameters.startswith("id=")):
        D.error_exit(f"Invalid Download URL: {url}\n(if this error shows up, that means I defined the url wrong. probably a typo or something)")
    
    #if the url has a valid format, then we wanna check if the url is valid like if it actually points to something
    try:
        response = requests.head(url, allow_redirects=True)  # Using HEAD to avoid downloading the file

        # Check if the URL returns a valid response code
        if response.status_code != 200:
            D.error_exit(f"Could not reach desired file. Status Code: {response.status_code} \n(if this error shows up, that means most likeley the url has become invalid and that I need to update the runstaller)")
    except requests.exceptions.RequestException as e:
        D.error_exit(f"An error occurred while checking the URL: {e}\n(if this error shows up, that means the url is not reachable or the file is not accessible this has most likely nothing to do with the runstaller and may just be your internet connection)")

def _download_from_drive(url, filename):
    _check_drive_url(url) #check if the url is valid
    try:
        output = gdown.download(url, os.path.join(M.TEMP, filename), quiet=True)
        if output is None:
            raise Exception("Download failed or file is not found.")
    except Exception as e:
        raise Exception(f"An error occurred while downloading the file: {e}")

#=================================== INSTALL ===================================#
def install_git():
    _temp_folder() #temp folder
    if C.check_git(): #check if git is already installed
        D.error("Git is already installed, can't install it again")
        return
    else:
        D.message("Installing Git")
        try:
            D.info("Downloading Git Installer... (please wait, this may take a while)")
            _download_from_drive(M.URL_GIT, M.FILENAME_GIT)
            if not os.path.exists(os.path.join(M.TEMP, M.FILENAME_GIT)): #check if the file exists
                D.error_exit("Git install failed\n(file not found)")
        except Exception as e:
            D.error_exit(f"An error occurred while Downloading the Git Installer: {e}")
        D.success("Git Installer Downloaded")
        try:
            D.info("Running Git Installer... (please wait, this may take a while)")
            subprocess.run([os.path.join(M.TEMP, M.FILENAME_GIT), "/NORESTART", "/NOCANCEL", "/VERYSILENT"], check=True)
        except Exception as e:
            D.error_exit(f"An error occurred while running the Git Installer: {e}")
        D.success("Git Successfully Installed")
        _delete_file(M.FILENAME_GIT) #delete the installer

def install_jdk():
    _temp_folder() #temp folder
    if C.check_jdk(): #check if jdk is already installed
        D.error("JDK is already installed, can't install it again")
        return
    else:
        D.message("Installing JDK")
        try:
            D.info("Downloading JDK Installer... (please wait, this may take a while)")
            _download_from_drive(M.URL_JDK, M.FILENAME_JDK)
            if not os.path.exists(os.path.join(M.TEMP, M.FILENAME_JDK)): #check if the file exists
                D.error_exit("JDK install failed\n(file not found)")
        except Exception as e:
            D.error_exit(f"An error occurred while Downloading the JDK Installer: {e}")
        D.success("JDK Installer Downloaded")
        try:
            D.info("Running JDK Installer... (please wait, this may take a while)")
            subprocess.run([os.path.join(M.TEMP, M.FILENAME_JDK), "/s"], check=True)
        except Exception as e:
            D.error_exit(f"An error occurred while running the JDK Installer: {e}")
        D.success("JDK Successfully Installed")
        _delete_file(M.FILENAME_JDK) #delete the installer



def install_modpack():
    if not C.check_mmc(): #check if multimc is installed
        D.error_exit("MultiMC not installed\n(can't install Modpack if MultiMC is not installed)")
    
    if C.check_modpack(): #check if modpack is already installed
        D.error("Modpack is already installed, can't install it again")
        return
    else:
        D.message("Installing Modpack")
        try:
            D.info("Cloning Modpack... (please wait, this may take a while)")
            subprocess.run(["git", "config", "--global", "--add", "safe.directory", M.LOCATION_MODPACK_DIR], check=True)
            subprocess.run(["git", "clone", M.MODPACK_REPO, M.LOCATION_MODPACK_DIR], check=True)

            #git lfs
            subprocess.run(["git", "lfs", "install"], cwd=M.LOCATION_MODPACK_DIR, check=True)
            subprocess.run(["git", "lfs", "pull"], cwd=M.LOCATION_MODPACK_DIR, check=True)

            if not os.path.exists(M.LOCATION_MODPACK_DIR):
                D.error_exit("Modpack install failed\n(Modpack directory not found)")
        except Exception as e:
            D.error_exit(f"An error occurred while cloning the Modpack: {e}")

#=================================== QOL ===================================# installing stuff that's nice to have but on fail will not stop the program

def qol_download_icon():
    _temp_folder() #temp folder
    if not C.check_mmc(): #check if multimc is installed
        D.error("MultiMC not installed\n(can't install icon if it's not installed)")
        return
    
    if C.qol_check_icon(): #check if modpack icon is already installed
        D.warning("Modpack Icon already installed")
        return
    else:
        try:
            D.info("Dowloading Modpack Icon...")
            _download_from_drive(M.URL_ICON, M.FILENAME_ICON)

            if not os.path.exists(os.path.join(M.TEMP, M.FILENAME_ICON)): #check if the file exists
                D.error_exit("Modpack Icon install failed\n(file not found)")
        except Exception as e:
            D.error_exit(f"An error occurred while Downloading the Modpack Icon: {e}")

        try:
            D.info("\"Installing\" Modpack Icon...")
            os.rename(os.path.join(M.TEMP, M.FILENAME_ICON), M.LOCATION_MODPACK_ICON) #move the icon to the correct location
        except Exception as e:
            D.error_exit(f"An error occurred while \"installing\" the Modpack Icon: {e}")
        D.success("Modpack Icon Successfully Installed")
