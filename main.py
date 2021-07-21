from job import isprocessrunning

import win32serviceutil
import win32service
import win32event
import servicemanager


import socket
import logging
import sys
import time

logging.basicConfig(filename="service.log", level=logging.DEBUG)

firstProcessName = 'in-co-test.exe'
firstProcessPath = 'E:\LINKS\data_chizzza_ss\inplay-control\in-co-test.exe'
secondProcessName = 'in-co-supp.exe'
secondProcessPath = 'E:\LINKS\data_chizzza_ss\inplay-support\in-co-supp.exe'

class WatchDogService(win32serviceutil.ServiceFramework):
    _svc_name_ = "incoWatchDog"
    _svc_display_name_ = "in-co WatchDog"
    _svc_description_ = "service, that check every 10 sec is in-co running, and if not - start it"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def main(self):

        """DO THE RUN STUFF HERE"""
        logging.info("SERVICE MAIN ENTERED !!")
        rc = None
        while rc != win32event.WAIT_OBJECT_0:
            isprocessrunning(firstProcessName, firstProcessPath)
            isprocessrunning(secondProcessName, secondProcessPath)
            rc = win32event.WaitForSingleObject(self.hWaitStop, 10000)
            time.sleep(10)
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STOPPED,
                              (self._svc_name_, ''))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(WatchDogService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(WatchDogService)
