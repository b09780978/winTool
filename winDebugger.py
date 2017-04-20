from ctypes import *
from winStructure import *

kernel32 = windll.kernel32

class debugger():
    
    def __init__(self):
        self.__h_process = None
        self.__h_thread = None
        self.__pid = None
        self.__debugger_active = False
        self.__context = None
        self.__exception = None
        self.__exception_address = None

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
            #raw_input("Press a key to continue...")
            #self.__debugger_active = False
            self.__h_thread = self.open_thread(debug_event.dwThreadId)
            self.__context = self.get_thread_context(self.__h_thread)
            print "[+] Event Code: %d" % debug_event.dwDebugEventCode
            print "[+] Thread ID: %d" % debug_event.dwThreadId

            if debug_event.dwDebugEventCode == EXCEPTION_DEBUG_EVENT:
                self.__exception = debug_event.u.Exception.ExceptionRecord.ExceptionCode
                self.__exception_address = debug_event.u.Exception.ExceptionRecord.ExceptionAddress
                if self.__exception == EXCEPTION_ACCESS_VIOLATION:
                    print "[+] Access Violation Detected"

                elif self.__exception == EXCEPTION_BREAKPOINT:
                    continue_status = self.exception_handler_breakpoint()

                elif self.__exception == EXCEPTION_GUARD_PAGE:
                    print "[+] Guard Page Access Detected"

                elif self.__exception == EXCEPTION_SINGLE_STEP:
                    #self.exception_handler_single_step()
                    print "[+] Single step"

            kernel32.ContinueDebugEvent(debug_event.dwProcessId,
                                        debug_event.dwThreadId,
                                        continue_status)

    # detach a process
    def detach(self):
        if kernel32.DebugActiveProcessStop(self.__pid):
            print "[+] Finished debugging."
            print "[+] Exiting..."
            return True
        else:
            print "[-] detach fail"
            print "[-] Error: %0x%08x" % kernel32.GetLastError()
            return False

    def open_thread(self, thread_id):
        h_thread = kernel32.OpenThread(THREAD_ALL_ACCESS, False, thread_id)

        if h_thread is not None:
            return h_thread
        else:
            print "[-] Could not OpenThread"
            return None

    # use CreateToolhelp32Snapshot to get snapshot and get debug thread
    def enumerate_threads(self):
        thread_entry = THREADENTRY32()
        thread_list = []
        snapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPTHTREAD, self.__pid)
        if snap is not None:
            thread_entry.dwSize = sizeof(thread_entry)
            success = kernel32.Thread32First(snapshot, byref(thread_entry))
            while success:
                if thread_entry.th32OwnerProcessID == self.__pid:
                    thread_list.append(thread_entry.th32OwnerProcessID)
                success = kernel32.Thread32Next(snapshot, byref(thread_entry))

            kernel32.CloseHandle(snapshot)
            return thread_list

    # get thread's context
    def get_thread_context(self, thread_id):
        context = CONTEXT()
        context.ContextFlags = CONTEXT_FULL | CONTEXT_DEBUG_REGISTERS

        h_thread = self.open_thread(thread_id)
        if kernel32.GetThreadContext(h_thread, byref(context)):
            kernel32.CloseHandle(h_thread)
            return context
        else:
            return None

    def exception_handler_breakpoint(self):
        print "[+] Inside breakpoint handler"
        print "[+] Exception Address 0x%08x" % self.__exception_address
        return DBG_CONTINUE
