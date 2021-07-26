import psutil


import subprocess
from logg import logg

def killProcess(processName):
    for process in psutil.process_iter():
        try:
            if processName.lower() in process.name().lower():
                process.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass



def startProcess(processPath):
    try:
        logg('TRYING TO START PROCESS')
        logg(processPath)
        proc = subprocess.Popen(processPath, shell=False)
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
        logg(processName + 'process doesn\'t run')
        startProcess(processPath)
        isExist = False