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

def _temp_folder(): #check if the temp folder exists and if not create it
    if not os.path.exists(M.TEMP):
        try:
            os.mkdir(M.TEMP)
        except Exception as e:
            D.error_exit(f"An error occurred while creating the temp folder: {e}")
    
def _delete_file(filename): #delete a file or directory
    try:
        filename = os.path.join(M.TEMP, filename) #make sure the file is in the temp folder
        if os.path.exists(filename):
            if os.path.isdir(filename):
                shutil.rmtree(filename, ignore_errors=True)
            else:
                os.remove(filename)
    except Exception as e:
        D.error(f"An error occurred while deleting the file: {e}")

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

def install_mmc():
    _temp_folder() #temp folder
    if C.check_mmc(): #check if multimc is already installed
        D.error("MultiMC is already installed, can't install it again")
        return
    else:
        D.message("Installing MultiMC")
        try:
            D.info("Downloading MultiMC \"Installer\"... (please wait, this may take a while)")
            _download_from_drive(M.URL_MMC, M.FILENAME_MMC)
            if not os.path.exists(os.path.join(M.TEMP, M.FILENAME_MMC)): #check if the file exists
                D.error_exit("MultiMC install failed\n(file not found)")
        except Exception as e:
            D.error_exit(f"An error occurred while Downloading the MultiMC Installer: {e}")
        D.success("MultiMC \"Installer\" Downloaded")
        try:
            D.info("\"Installing\" MultiMC... (please wait, this may take a while)")

            #the "install" process for multimc is a bit different since it's a zip file.
            #so we downloaded a zipfile called "mmc.zip". that zipfile contains the MultiMC folder, that folder contains the program.
            #so what we wanna do is extract the MultiMC folder from the zipfile and move it to the correct location.
            #that being %localappdata%/Programs. so we end up with %localappdata%/Programs/MultiMC

            #check if the folder we want to extact to even exists.
            if not os.path.exists(os.path.dirname(M.LOCATION_MMC_DIR)):
                D.error_exit("MultiMC install failed\n(Programs directory not found)")

            with zipfile.ZipFile(os.path.join(M.TEMP, M.FILENAME_MMC), "r") as zip_ref:
                zip_ref.extractall(M.LOCATION_MMC_DIR) #extract the files to the MultiMC directory

            if not os.path.exists(M.LOCATION_MMC_DIR) or not os.path.exists(M.LOCATION_MMC_EXE):
                D.error_exit("MultiMC install failed\n(MultiMC probaly not correctly extracted)")
        except Exception as e:
            D.error_exit(f"An error occurred while \"installing\" MultiMC: {e}")
        D.success("MultiMC Successfully Installed")
        _delete_file(M.FILENAME_MMC) #delete the installer

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
def qol_configure_mmc():
    if not C.check_mmc(): #check if multimc is installed
        D.error("MultiMC not installed\n(can't configure MultiMC if it's not installed)")
        return
    
    if C.qol_check_config(): #check if multimc is already configured
        D.warning("MultiMC already configured")
        return
    else:
        try:
            D.info("Configuring MultiMC...")

            with open(os.path.join(M.LOCATION_MMC_DIR, "multimc.cfg"), "w") as f: #create the config file and write the settings
                f.write("JavaVersion=17.0.11\n")
                f.write("JavaPath=C:/Program Files/Java/jdk-17/bin/javaw.exe\n")
                f.write("Language=en_US\n")
                f.write(f"LastHostname={os.getenv('COMPUTERNAME')}\n")
                f.write("ShownNotifications=")
        except Exception as e:
            D.error(f"An error occurred while configuring MultiMC: {e}")
        try:
            D.info("Applying Config...")

            #so the settings get applied we still need to start MultiMc once let it cope the settings and then close it prefferebly we don't want to distract the user so it would be nice to start it minimized
            subprocess.Popen([M.LOCATION_MMC_EXE], creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(1)
            subprocess.run(["taskkill", "/IM", "MultiMC.exe", "/F"], check=True)

        except Exception as e:
            D.error(f"An error occurred while applying the configs: {e}")
        D.success("MultiMC Successfully Configured")

def qol_create_mmc_shortcut():
    if not C.check_mmc(): #check if multimc is installed
        D.error("MultiMC not installed\n(can't create MultiMC shortcut if it's not installed)")
        return
    
    if C.qol_ckeck_shortcut(): #check if multimc shortcut is already created
        D.warning("MultiMC shortcut already created")
        return
    else:
        try:
            D.info("Creating MultiMC Shortcut...")
            subprocess.run(["powershell", "-Command", f"$s=(New-Object -COM WScript.Shell).CreateShortcut('{M.LOCATION_MMC_SHORTCUT}');$s.TargetPath='{M.LOCATION_MMC_EXE}';$s.Save()"], check=True)
        except Exception as e:
            D.error(f"An error occurred while creating the MultiMC Shortcut: {e}")
        D.success("MultiMC Shortcut Successfully Created")
    
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
