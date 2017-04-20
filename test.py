import winDebugger

debugger = winDebugger.debugger()
#debugger.load("C:\Windows\System32\calc.exe")
pid = raw_input("Enter pid: ")
debugger.attach(int(pid))
thread_list = debugger.enumerate_threads()

for thread in thread_list:
    thread_context = debugger.get_thread_context(thread)
    print "[+] Dumping registers for thread ID: 0x%08x" % thread
    print "[+] EIP: 0x%08x" % thread_context.Eip
    print "[+] ESP: 0x%08x" % thread_context.Esp
    print "[+] EBP: 0x%08x" % thread_context.Ebp
    print "[+] EAX: 0x%08x" % thread_context.Eax
    print "[+] EBX: 0x%08x" % thread_context.Ebx
    print "[+] ECX: 0x%08x" % thread_context.Ecx
    print "[+] EDX: 0x%08x" % thread_context.Edx
    print "[+] Dump finish"

debugger.detach()

