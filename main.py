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


class ExampleService(win32serviceutil.ServiceFramework):
    _svc_name_ = "AExampleService"
    _svc_display_name_ = "AExample Service"
    _svc_description_ = "Example description"

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
            isprocessrunning()
            rc = win32event.WaitForSingleObject(self.hWaitStop, 10000)
            time.sleep(30)
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STOPPED,
                              (self._svc_name_, ''))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(ExampleService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(ExampleService)
