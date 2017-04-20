import winDebugger

debugger = winDebugger.debugger()
pid = raw_input("Enter pid: ")
debugger.attach(int(pid))
debugger.detach()
