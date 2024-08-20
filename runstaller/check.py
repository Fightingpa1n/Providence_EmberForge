import subprocess
import os

import main as M

def _check_using_version(program):
    try:
        params = (program.split("_") if "_" in program else [program]) + ["--version"]
        subprocess.run(params, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
    
#=================================== CHECKS ===================================#
def check_git() -> bool:
    return _check_using_version("git")

def check_jdk() -> bool:
    return _check_using_version("java") and _check_using_version("javac")

def check_mmc() -> bool:
    return os.path.exists(M.LOCATION_MMC_DIR) and os.path.exists(M.LOCATION_MMC_EXE)

def check_modpack() -> bool:
    return os.path.exists(M.LOCATION_MODPACK_DIR)

#=================================== QOL ===================================#
def qol_check_config() -> bool:
    return os.path.join(M.LOCATION_MMC_DIR, "multimc.cfg")

def qol_ckeck_shortcut() -> bool:
    return os.path.exists(M.LOCATION_MMC_SHORTCUT)

def qol_check_icon() -> bool:
    return os.path.exists(M.LOCATION_MODPACK_ICON)
