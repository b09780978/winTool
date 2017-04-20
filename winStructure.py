from ctypes import *

# define windows data type
WORD    =   c_ushort
DWORD   =   c_ulong
LPBYTE  =   POINTER(c_ubyte)
LPTSTR  =   POINTER(c_char)
HANDLE  =   c_void_p
PVOID   =   c_void_p
UINT_PTR=   c_ulong

# define windows flags contents

# Process Creation Flags
DEBUG_PROCESS            =       0x00000001

# dwFlags Flags
STARTF_USESHOWWINDOW     =       0x00000001

# CmdShow Flags
SW_HIDE                  =       0x00000000

# Process Access Flags
PROCESS_ALL_ACCESS = 0x001f0fff

# Debug continue Flags
DBG_CONTINUE = 0x00010002

# WaitForDebugEvent time
INFINITE = 0xffffffff


# define windows data structure
# debugger will need to use

class STARTUPINFO(Structure):
    _fields_ = [
        ("cb"               ,       DWORD),
        ("lpReserved"       ,      LPTSTR),
        ("lpDesktop"        ,      LPTSTR),
        ("lpTitle"          ,      LPTSTR),
        ("dwX"              ,       DWORD),
        ("dwY"              ,       DWORD),
        ("dwXSize"          ,       DWORD),
        ("dwYSize"          ,       DWORD),
        ("dwXCountChars"    ,       DWORD),
        ("dwYCountChars"    ,       DWORD),
        ("dwFillAttribute"  ,       DWORD),
        ("dwFlags"          ,       DWORD),
        ("wShowWindow"      ,        WORD),
        ("cbReserved2"      ,        WORD),
        ("lpReserved2"      ,      LPBYTE),
        ("hStdInput"        ,      HANDLE),
        ("hStdOutput"       ,      HANDLE),
        ("hStdError"        ,      HANDLE)
        ]

class PROCESS_INFORMATION(Structure):
    _fields_ = [
        ("hProcess"         ,       HANDLE),
        ("hThread"          ,       HANDLE),
        ("dwProcessId"      ,        DWORD),
        ("dwThreadId"       ,        DWORD)
        ]

# because EXCEPTION_RECORD need to define self pointer
# _fields_ need to fill latter
class EXCEPTION_RECORD(Structure):
    pass


EXCEPTION_RECORD._fields_ = [
    ("ExceptionCode"    ,        DWORD),
    ("ExceptionFlags"   ,        DWORD),
    ("ExceptionRecord"  ,   POINTER(EXCEPTION_RECORD)),
    ("ExceptionAddress" ,           PVOID),
    ("NumberParameters" ,        DWORD),
    ("ExceptionInformatin",     UINT_PTR * 15)
    ]

#class EXCEPTION_RECORD(Structure):
#    _fields_ = [
#    ("ExceptionCode"    ,        DWORD),
#    ("ExceptionFlags"   ,        DWORD),
#    ("ExceptionRecord"  ,   POINTER(EXCEPTION_RECORD),
#    ("ExceptionAddress" ,           PVOID),
#    ("NumberParameters" ,        DWORD),
#    ("ExceptionInformatin",     UINT_PTR * 15)
#    ]
    
class EXCEPTION_DEBUG_INFO(Structure):
    _fields_ = [
        ("ExceptionRecord"  ,   EXCEPTION_RECORD),
        ("dwFirstChance"    ,              DWORD)
        ]

# this union has many structure
# but in this book only use exception
class DEBUG_EVENT_UNION(Structure):
    _fields_ = [
        ("Exception"        ,       EXCEPTION_DEBUG_INFO),
       # ("CreateThread"     ,       CREATE_THREAD_DEBUG_INFO),
       # ("CreateProcessInfo",       CREATE_PROCESS_DEBUG_INFO),
       # ("ExitThread"       ,       EXIT_THREAD_DEBUG_INFO),
       # ("ExitProcess"      ,       EXIT_PROCESS_DEBUG_INFO),
       # ("LoadDll"          ,       LOAD_DLL_DEBUG_INFO),
       # ("UNLOADll"         ,       UNLOAD_DLL_DEBUG_INFO),
       # ("DebugString"      ,       OUTPUT_DEBUG_STRING_INFO),
       # ("RipInfo"          ,       RIP_INFO)
        ]

class DEBUG_EVENT(Structure):
    _fields_ = [
        ("dwDebugEnentCode"  ,       DWORD),
        ("dwProcessId"       ,       DWORD),
        ("dwThreadId"        ,       DWORD),
        ("u"                 ,DEBUG_EVENT_UNION) 
        ]


