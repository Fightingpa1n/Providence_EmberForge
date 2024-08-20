import argparse
import os
import shutil
import subprocess

import debug as D #import the debug module
import check as C #import the check module
import install as I #import the install module

#this is the main script that gets executed when the runstaller is run.
#it's responsible for checking if everything is installed correctly and working, and if not it should install it,
#and once everything is installed correctly, it should run the main program.
#and if everything is installed correctly from the start, it should just run the main program.

#=================================== VARS ===================================#
MODPACK_REPO = "https://github.com/Fightingpa1n/Providence_modpack.git" #link to the modpack repository
MODPACK_NAME = "Providence_EmberForge" #name of the modpack
MODPACK_ICON = "providence_icon.png" #filename of the modpack icon

FILENAME_GIT = "git_installer.exe" #filename of the git installer
FILENAME_JDK = "jdk_installer.exe" #filename of the jdk installer
FILENAME_MMC = "mmc.zip" #filename of the multimc "installer" (it's just a zip file)

URL_GIT = "https://drive.google.com/uc?id=17FDn41yqIeXiqQDKIo3BsnbWniaijZZF" #url to drive download
URL_JDK = "https://drive.google.com/uc?id=1_O53V7ATJ7og3E3_5jTF8BFFqQ12G7Fg" #url to drive download
URL_MMC = "https://drive.google.com/uc?id=1H-Dp5h7A4uUspNCDu_O0MBGo8psWt_B0" #url to drive download
URL_ICON = "https://drive.google.com/uc?id=1R3deuIf0PpdeKeqpSrEgUxCB64YYmIct" #url to drive download

#=================================== PATHS ===================================#
ROAMING = os.getenv("APPDATA") #roaming directory
LOCAL = os.getenv("LOCALAPPDATA") #local directory

TEMP = os.path.join(ROAMING, ".providence_runstaller_temp") #temporary location for the files in the appdata folder

#=================================== LOCATIONS ===================================#
LOCATION_MMC_DIR = os.path.join(LOCAL, "Programs", "MultiMC") #location of the MultiMC directory
LOCATION_MMC_EXE = os.path.join(LOCATION_MMC_DIR, "MultiMC.exe") #location of the MultiMC executable
LOCATION_MMC_SHORTCUT = os.path.join(ROAMING, "Microsoft", "Windows", "Start Menu", "Programs", "MultiMC.lnk") #location of the MultiMC shortcut
LOCATION_MODPACK_DIR = os.path.join(LOCATION_MMC_DIR, "instances", MODPACK_NAME) #location of the modpack directory
LOCATION_MODPACK_ICON = os.path.join(LOCATION_MMC_DIR, "icons", MODPACK_ICON) #location of the modpack icon

#=================================== FUNCTIONS ===================================#

def check(): #check if everything is installed
    git = C.check_git()
    jdk = C.check_jdk()
    mmc = C.check_mmc()
    modpack = C.check_modpack()
    return git and jdk and mmc and modpack

def install(): #install everything that's missing
    D.message("Starting installation")

    if not D.is_admin():
        D.error_exit("Please run as Administrator (installation requires admin rights)")
    
    try:
        if not C.check_git():
            D.info("Git was not found, installing Git")
            I.install_git()
            D.success("Git was installed successfully")
            D.info("due to changing of PATH variables, a restart is required. after exiting, please run the runstaller again")
            D.wait_exit()
        if not C.check_jdk():
            D.info("JDK was not found, installing JDK")
            I.install_jdk()
            D.success("JDK was installed successfully")
            D.info("java was just installed and due to it having special needs, you need to restart your pc before you can continue")
            D.wait_exit()

        if not C.check_mmc():
            D.info("MultiMC was not found, installing MultiMC")
            I.install_mmc()
            D.success("MultiMC was installed successfully")
        if not C.check_modpack():
            D.info("Modpack was not found, installing Modpack")
            I.install_modpack()
            D.success("Modpack was installed successfully")
    except Exception as e:
        D.error_exit(f"Installation failed: {e} (somthing in the installation process went wrong, please try again)")
    if not check():
        D.error_exit("Not everything was installed correctly, please try again")

    qol()
    D.success("Installation completed")

def qol():
    if not check():
        try:
            if not C.qol_check_config():
                I.qol_configure_mmc()
            if not C.qol_ckeck_shortcut():
                I.qol_create_shortcut()
            if not C.qol_check_icon():
                I.qol_download_icon()
        except Exception as e:
            D.warning(f"QOL failed: {e} \n(an error accoured while trying to apply QOL stuff, since QOL is not critical, we will continue)")
    
    try: #remove the temp folder
        if os.path.exists(TEMP):
            shutil.rmtree(TEMP, ignore_errors=True)
    except Exception as e:
        D.warning(f"Failed to remove temp folder: {e}")

def update_modpack(): #update the modpack
    if not C.check_modpack():
        D.error_exit("Modpack was not found, can't update")
    
    D.message("Checking for updates")
    try:
        os.chdir(LOCATION_MODPACK_DIR) #change dir
        
        # Step 1: Fetch the latest changes from the remote repository
        subprocess.run(["git", "fetch"], check=True)
        
        # Step 2: Check if the local branch is up-to-date with the remote branch
        result = subprocess.run(["git", "status", "-uno"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if b"Your branch is up to date" in result.stdout:
            D.info("Modpack is up to date.")
        else:
            D.info("Newer version found. Updating modpack...")
            try:
                # Step 3: Attempt to pull the latest changes
                subprocess.run(["git", "pull"], check=True)
                D.success("Modpack updated successfully.")
            except subprocess.CalledProcessError:
                D.warning("Conflict detected. Resolving by discarding local changes...")
                
                # Step 4: Discard local changes and pull again
                subprocess.run(["git", "reset", "--hard", "HEAD"], check=True)
                subprocess.run(["git", "pull"], check=True)
                D.success("Modpack updated successfully after resolving conflicts.")
    except Exception as e:
        D.error(f"Failed to update modpack: {e}\nplease try again (if this error persists, you may need to delete the modpack folder)")
        D.warning(f" Modpack directory: {LOCATION_MODPACK_DIR}. WARNING! deleting this folder will reset any client options, saves, maps, etc.")

def start_modpack(): #start the modpack
    if not C.check_modpack():
        D.error_exit("Modpack was not found, can't start")
    update_modpack()

    subprocess.Popen(
        ["cmd", "/c", "start", "", LOCATION_MMC_EXE, "--launch", MODPACK_NAME],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    D.message("Starting Modpack... (please wait, this may take a while)")

    D.message("the modpack should start shortly (you may still need to wait a bit)")
    D.info("this window should close itself. (If it doesn't, you can close it manually)")
    D.exit()

#=================================== MAIN ===================================#
if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Runstaller")
        parser.add_argument("--install", action="store_true", help="Start the installer") #if we run with --install we automatically start the installer
        parser.add_argument("--run", action="store_true", help="Start The Modpack") #if we run with --run we automatically run the main program

        args = parser.parse_args() #parse the arguments

        if args.run and args.install: #if we run with both --run and --install
            D.error_exit("You can't run and install at the same time")

        if args.run: #if we wanna run the main program
            if not check():
                D.error_exit("can't run the main program, since not every required component is installed")
            else:
                start_modpack()
        elif args.install: #if we wanna run the installer
            if check():
                qol()
                D.error_exit("Everything is already installed")
            else:
                install()
                D.wait_exit()
        else: #if we don't run with any arguments
            if not check():
                D.info("Not everything is installed, starting the installer")
                install()
                answer = D.prompt("start Modpack? [y/n]", "y").lower()
                if answer == "y":
                    start_modpack()
                else:
                    D.info("Exiting the program (now that everything is installed running this program again will start the modpack)")
                    D.exit()
            else:
                qol()
                D.message("Everything is installed, starting the main program")
                start_modpack()
    except Exception as e: #if anything goes wrong isnstead of just crashing, we print the error and wait for the user to press enter before exiting
        print(f"FATAL ERROR ENCOUNTERED:\n{e}")
        input("Press enter to exit")
