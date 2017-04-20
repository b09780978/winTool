from ctypes import *

# define windows data type
WORD    =   c_ushort
DWORD   =   c_ulong
LPBYTE  =   POINTER(c_ubyte)
LPTSTR  =   POINTER(c_char)
HANDLE  =   c_void_p

# define windows flags contents

# Process Creation Flags
DEBUG_PROCESS            =       0x00000001

# dwFlags Flags
STARTF_USESHOWWINDOW     =       0x00000001

# CmdShow Flags
SW_HIDE                  =       0x00000000


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
