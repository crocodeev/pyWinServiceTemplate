import psutil

import win32ts
import win32profile
import win32process
import win32con

def startProcess(processPath):
        # 1. GET USER TOKEN
        console_session_id = win32ts.WTSGetActiveConsoleSessionId()
        console_user_token = win32ts.WTSQueryUserToken(console_session_id)

        # 2. GET THIS USER'S ENVIRONMENT
        environment = win32profile.CreateEnvironmentBlock(console_user_token, False)

        # 3. GENERATE STARTUPINFO FOR THE PROCESS ( OPTIONAL )
        startupInfo = win32process.STARTUPINFO()
        # OPTIONAL
        startupInfo.dwFlags = win32process.STARTF_USESHOWWINDOW
        startupInfo.wShowWindow = win32con.SW_NORMAL

        # 4. CREATE PROCESS AS USER
        win32process.CreateProcessAsUser(console_user_token,
                                         processPath,
                                         None,
                                         None,
                                         None,
                                         0,
                                         win32con.NORMAL_PRIORITY_CLASS,
                                         environment,
                                         None,
                                         startupInfo)


def isprocessrunning(processName, processPath):
    isExist = False
    for process in psutil.process_iter():
        try:
            if processName.lower() in process.name().lower():
                isExist = True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    if isExist == False:
        startProcess(processPath)
        isExist = False

