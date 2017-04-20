from ctypes import *
from winStructure import *

kernel32 = windll.kernel32

class debugger():
    
    def __init__(self):
        self.__h_process = None
        self.__pid = None
        self.__debugger_active = False

    # load a file path, use CreateProcessA function to open it
    # and use another process to debug it
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
            # open a process for debug
            self.__h_process = self.open_process(process_infomation.dwProcessId)

        else:
            print "[-] Fail!"
            print "[-] Error: 0x%08x" % kernel32.GetLastError()

    # call OpenProcess function to generate a debug process(with all access)
    def open_process(self, pid):
        h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
        return h_process

    # open a debug process and attach the file's pid
    def attach(self, pid):
        self.__h_process = self.open_process(pid)
        # try to attach file
        if kernel32.DebugActiveProcess(pid):
            self.__debugger_active = True
            self.__pid = int(pid)
            self.run()

        else:
            print "[-] Unable to attach process"

    # run and wait for accept debug event
    def run(self):
        while self.__debugger_active:
            self.get_debug_event()

    # use a DEBUG_EVENT to catch all event
    def get_debug_event(self):
        debug_event = DEBUG_EVENT()
        continue_status = DBG_CONTINUE

        if kernel32.WaitForDebugEvent(byref(debug_event), INFINITE):
            raw_input("Press a key to continue...")
            self.__debugger_active = False
            kernel32.ContinueDebugEvent(debug_event.dwProcessId,
                                        debug_event.dwThreadId,
                                        continue_status)

    def detach(self):
        if kernel32.DebugActiveProcessStop(self.__pid):
            print "[+] Finished debugging."
            print "[+] Exiting..."
            return True
        else:
            print "[-] detach fail"
            print "[-] Error: %0x%08x" % kernel32.GetLastError()
            return False
