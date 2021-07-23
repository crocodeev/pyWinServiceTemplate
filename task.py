import psutil


import subprocess
from logg import logg



def startProcess(processPath):
    try:
        logg('TRYING TO START PROCESS')
        subprocess.Popen(processPath, shell=True)
    except Exception as e:
        logg(e)



def isprocessrunning(processName, processPath):
    isExist = False
    for process in psutil.process_iter():
        try:
            if processName.lower() in process.name().lower():
                isExist = True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    if isExist == False:
        logg(processName + ' doesn\'t exist')
        startProcess(processPath)
        isExist = False