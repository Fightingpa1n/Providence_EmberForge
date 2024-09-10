import os
import subprocess
import zipfile
import time

import main as Main
import misc as Misc
import debug as Debug

#This File contains all the functions that handle the installation of MultiMC

MMC_FILE = "mmc.zip" #name of the MultiMC "installer" file

MMC_DIR = os.path.join(Misc.LOCAL, "Programs", "MultiMC") #location of the MultiMC directory
MMC_EXE = os.path.join(MMC_DIR, "MultiMC.exe") #location of the MultiMC executable
MMC_SHORTCUT = os.path.join(Misc.ROAMING, "Microsoft", "Windows", "Start Menu", "Programs", "MultiMC.lnk") #location of the MultiMC shortcut


def is_installed():
    return os.path.exists(MMC_DIR) and os.path.exists(MMC_EXE)

def has_shortcut():
    return os.path.exists(MMC_SHORTCUT)

def install_mmc():
    Misc.temp() #temp folder
    if is_installed(): #check if multimc is already installed
        Debug.warning("MultiMC is already installed")
        return
    else:
        Debug.message("Installing MultiMC")
        try:
            Debug.info("Downloading MultiMC \"Installer\"... (please wait, this may take a while)")

            if not os.path.exists(os.path.join(Main.TEMP, Main.FILENAME_MMC)): #check if the file exists
                Debug.error_exit("MultiMC install failed\n(file not found)")
        except Exception as e:
            Debug.error_exit(f"An error occurred while Downloading the MultiMC Installer: {e}")
        Debug.success("MultiMC \"Installer\" Downloaded")
        try:
            Debug.info("\"Installing\" MultiMC... (please wait, this may take a while)")

            #the "install" process for multimc is a bit different since it's a zip file.
            #so we downloaded a zipfile called "mmc.zip". that zipfile contains the MultiMC folder, that folder contains the program.
            #so what we wanna do is extract the MultiMC folder from the zipfile and move it to the correct location.
            #that being %localappdata%/Programs. so we end up with %localappdata%/Programs/MultiMC

            #check if the folder we want to extact to even exists.
            if not os.path.exists(os.path.dirname(Main.LOCATION_MMC_DIR)):
                Debug.error_exit("MultiMC install failed\n(Programs directory not found)")

            with zipfile.ZipFile(os.path.join(Main.TEMP, Main.FILENAME_MMC), "r") as zip_ref:
                zip_ref.extractall(Main.LOCATION_MMC_DIR) #extract the files to the MultiMC directory

            if not os.path.exists(Main.LOCATION_MMC_DIR) or not os.path.exists(Main.LOCATION_MMC_EXE):
                Debug.error_exit("MultiMC install failed\n(MultiMC probaly not correctly extracted)")
        except Exception as e:
            Debug.error_exit(f"An error occurred while \"installing\" MultiMC: {e}")
        Debug.success("MultiMC Successfully Installed")
        _delete_file(Main.FILENAME_MMC) #delete the installer


def qol_configure_mmc():
    if not is_installed(): #check if multimc is installed
        Debug.error("MultiMC not installed\n(can't configure MultiMC if it's not installed)")
        return
    
    if C.qol_check_config(): #check if multimc is already configured
        Debug.warning("MultiMC already configured")
        return
    else:
        try:
            Debug.info("Configuring MultiMC...")

            with open(os.path.join(Main.LOCATION_MMC_DIR, "multimc.cfg"), "w") as f: #create the config file and write the settings
                f.write("JavaVersion=17.0.11\n")
                f.write("JavaPath=C:/Program Files/Java/jdk-17/bin/javaw.exe\n")
                f.write("Language=en_US\n")
                f.write(f"LastHostname={os.getenv('COMPUTERNAME')}\n")
                f.write("ShownNotifications=")
        except Exception as e:
            Debug.error(f"An error occurred while configuring MultiMC: {e}")
        try:
            Debug.info("Applying Config...")

            #so the settings get applied we still need to start MultiMc once let it cope the settings and then close it prefferebly we don't want to distract the user so it would be nice to start it minimized
            subprocess.Popen([Main.LOCATION_MMC_EXE], creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(1)
            subprocess.run(["taskkill", "/IM", "MultiMC.exe", "/F"], check=True)

        except Exception as e:
            Debug.error(f"An error occurred while applying the configs: {e}")
        Debug.success("MultiMC Successfully Configured")

def create_shortcut():
    if not is_installed(): #check if multimc is installed
        Debug.error("MultiMC not installed\n(can't create MultiMC shortcut if it's not installed)")
        return
    
    if C.qol_ckeck_shortcut(): #check if multimc shortcut is already created
        Debug.warning("MultiMC shortcut already created")
        return
    else:
        try:
            Debug.info("Creating MultiMC Shortcut...")
            subprocess.run(["powershell", "-Command", f"$s=(New-Object -COM WScript.Shell).CreateShortcut('{M.LOCATION_MMC_SHORTCUT}');$s.TargetPath='{Main.LOCATION_MMC_EXE}';$s.Save()"], check=True)
        except Exception as e:
            Debug.error(f"An error occurred while creating the MultiMC Shortcut: {e}")
        Debug.success("MultiMC Shortcut Successfully Created")
    
