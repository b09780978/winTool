from ctypes import *

# define windows data type
BYTE    =   c_ubyte
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

# Thread Access Flag
THREAD_ALL_ACCESS = 0x001f03ff

# Debug continue Flags
DBG_CONTINUE = 0x00010002

# WaitForDebugEvent time
INFINITE = 0xffffffff

# CreateToolhelp32Snapshot Flags
TH32CS_INHERIT = 0x80000000
TH32CS_SNAPHEAPLIST = 0x000001
TH32CS_SNAPMODULE = 0x00000008
TH32CS_SNAPMODULE32 = 0x00000010
TH32CS_SNAPPROCESS = 0x00000002
TH32CS_SNAPTHREAD = 0x00000004
TH32CS_SNAPALL = ( TH32CS_SNAPHEAPLIST | TH32CS_SNAPPROCESS | TH32CS_SNAPTHREAD | TH32CS_SNAPMODULE)

# Context Flags
CONTEXT_FULL = 0x00010007
CONTEXT_DEBUG_REGISTERS = 0x00010010

# EXCEPTION handler
EXCEPTION_ACCESS_VIOLATION = 0xc0000005
EXCEPTION_BREAKPOINT       = 0x80000003
EXCEPTION_BUARD_PAGE       = 0x80000001
EXCEPTION_SINGLE_STEP      = 0x80000004

# EVENT handler
EXCEPTION_DEBUG_EVENT       = 0x1
CREATE_THREAD_DEBUG_EVENT   = 0x2
CREATE_PROCESS_DEBUG_EVENT  = 0x3
EXIT_THREAD_DEBUG_EVENT     = 0x4
EXIT_PROCESS_DEBUG_EVENT    = 0x5
LOAD_DLL_DEBUG_EVENT        = 0x6
UNLOAD_DLL_DEBUG_EVENT      = 0x7
OUTPUT_DEBUG_STRING_EVENT   = 0x8
RIP_EVENT                   = 0x9

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
        ("dwDebugEventCode"  ,       DWORD),
        ("dwProcessId"       ,       DWORD),
        ("dwThreadId"        ,       DWORD),
        ("u"                 ,DEBUG_EVENT_UNION) 
        ]

class THREADENTRY(Structure):
    _fields_ = [
        ("dwSize"            ,       DWORD),
        ("cntUsage"          ,       DWORD),
        ("th32ThreadID"      ,       DWORD),
        ("th32OwnerProcessID",       DWORD),
        ("tpBasePri"         ,       DWORD),
        ("tpDeltaPri"        ,       DWORD),
        ("dwFlags"           ,       DWORD)
        ]


class FLOATING_SAVE_AREA(Structure):
    _fields_ = [
        ("ControlWord"       ,       DWORD),
        ("StatusWord"        ,       DWORD),
        ("TagWord"           ,       DWORD),
        ("ErrorOffset"       ,       DWORD),
        ("ErrorSelector"     ,       DWORD),
        ("DataOffset"        ,       DWORD),
        ("DataSelector"      ,       DWORD),
        ("RegisterArea"      ,   BYTE * 80),
        ("Cr0NpxState"       ,       DWORD)
        ]

class CONTEXT(Structure):
    _fields_ = [
        ("ContextFlags"      ,       DWORD),
        ("Dr0"               ,       DWORD),
        ("Dr2"               ,       DWORD),
        ("Dr3"               ,       DWORD),
        ("Dr6"               ,       DWORD),
        ("Dr7"               ,       DWORD),
        ("FloatSave"         ,  FLOATING_SAVE_AREA),
        ("sEGGs"             ,       DWORD),
        ("sEGFs"             ,       DWORD),
        ("sEGEs"             ,       DWORD),
        ("sEGDs"             ,       DWORD),
        ("Edi"               ,       DWORD),
        ("Esi"               ,       DWORD),
        ("Ebx"               ,       DWORD),
        ("Edx"               ,       DWORD),
        ("Ecx"               ,       DWORD),
        ("Eax"               ,       DWORD),
        ("Ebp"               ,       DWORD),
        ("Eip"               ,       DWORD),
        ("SegCs"             ,       DWORD),
        ("EFlags"            ,       DWORD),
        ("Esp"               ,       DWORD),
        ("SegSs"             ,       DWORD),
        ("ExtendeRegisters"  ,  BYTE * 512)
        ]
