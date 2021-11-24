from task import isprocessrunning, killProcess

import win32serviceutil
import win32service
import win32event
import win32timezone
import servicemanager

import socket
import sys
import time

from logg import logg

processArray = [('in-co-test.exe', 'E:\\LINKS\\data_chizzza_ss\\inplay-control\\in-co-test.exe'),
                ('in-co-supp.exe', 'E:\\LINKS\\data_chizzza_ss\\inplay-support\\in-co-supp.exe'),
                ('mediaroom3.exe', 'E:\\LINKS\\data_chizzza_ss\\mediaroom3.exe')]

processArray2 = [('testWebServer.exe', 'C:\\incoWatchDog\\testWebServer.exe')]


class WatchDogService(win32serviceutil.ServiceFramework):
    _svc_name_ = "incoWatchDog"
    _svc_display_name_ = "in-co WatchDog"
    _svc_description_ = "service, that check every 10 sec is in-co running, and if not - start it"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcDoRun(self):
        logg("SERVICE IS STARTING...")
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def SvcStop(self):
        logg("SERVICE CALLED TO STOP")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.stop()

    def stop(self):
        logg("START KILLING PROCESSES")
        for process in processArray:
            try:
                killProcess(process[0])
            except Exception as e:
                logg("Error when stop " + process[0])

    def main(self):

        """DO THE RUN STUFF HERE"""
        logg("SERVICE MAIN ENTERED !!")
        rc = None
        while rc != win32event.WAIT_OBJECT_0:
            for process in processArray:
                isprocessrunning(process[0], process[1])
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
