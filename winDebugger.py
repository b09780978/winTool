from ctypes import *
from winStructure import *

kernel32 = windll.kernel32

class debugger():
    
    def __init__(self):
        pass

    def load(self, file_path):
        # set create process flag to a debug process
        # this can receive all debug event from WaitForDebugEvent function
        create_flags = DEBUG_PROCESS

        # create a new STARTUPINFO structure
        # and set hide fiel_path window,
        # and activates another window
        startupinfo = STARTUPINFO()
        startupinfo.dwflags = STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = SW_HIDE
        startupinfo.cb = sizeof(STARTUPINFO)
        
        process_infomation = PROCESS_INFORMATION()

        if kernel32.CreateProcessA(file_path,
                                    None,
                                    None,
                                    None,
                                    None,
                                    create_flags,
                                    None,
                                    None,
                                    byref(startupinfo),
                                    byref(process_infomation)
                                    ):
            print "[+] Successfully launch the process!"
            print "[+] PID : %d" % process_infomation.dwProcessId

        else:
            print "[-] Fail!"
            print "[-] Error: 0x%08x" % kernel32.GetLastError()
