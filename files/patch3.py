import sys, struct, shutil
import pefile
from keystone import Ks, KS_ARCH_X86, KS_MODE_32, KS_OPT_SYNTAX_INTEL
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

SRC = r"C:\Program Files (x86)\Koei\San9 Tc\San9PK.exe"
DST = sys.argv[1] if len(sys.argv) > 1 else r".\San9PK_copilot.exe"

ks = Ks(KS_ARCH_X86, KS_MODE_32); ks.syntax = KS_OPT_SYNTAX_INTEL
md = Cs(CS_ARCH_X86, CS_MODE_32)

DRIVER    = 0x004C6C90
PICK_ORIG = 0x00570380
MULTI_PICK = 0x00570500      # checkbox multi-select picker (fills output list)
COLS_TANSAKU = 0x0066C694    # 探索 column data
NEW_OP    = 0x005DEC20
CMD_CTOR  = 0x00493EA0
GLOBAL_OFFICERS = 0x015455AC # global officer list the command commits
APPEND_FN = 0x0046EF70       # list push_back (thiscall: ecx=list, arg=value)
EXEC_ORIG = 0x00493F90       # 探索 command execute (builds one search unit for head officer)
VT_EXEC   = 0x00608554       # 探索 command vtable[11] slot -> EXEC_ORIG
DRV_CONT  = 0x004C6D3C

VT_SLOT   = 0x00609FC0
SITE_PICK = 0x004EC414
SITE_CTRLTYPE = 0x004EC3FB   # 'push 0x1E' (single ctrl) -> 'push 0x1C' (multi ctrl)
SITE_DRV  = 0x004C6D04

shutil.copy2(SRC, DST)
pe = pefile.PE(DST)
IB = pe.OPTIONAL_HEADER.ImageBase
FA = pe.OPTIONAL_HEADER.FileAlignment
SA = pe.OPTIONAL_HEADER.SectionAlignment
secs = [(s.Name.rstrip(b"\x00"), s.VirtualAddress, s.Misc_VirtualSize, s.PointerToRawData, s.SizeOfRawData) for s in pe.sections]
LAST_RVA = pe.sections[-1].VirtualAddress
LAST_VSZ = pe.sections[-1].Misc_VirtualSize
E_LFANEW = pe.DOS_HEADER.e_lfanew
SIZE_OPT = pe.FILE_HEADER.SizeOfOptionalHeader
NUM_SEC  = pe.FILE_HEADER.NumberOfSections
pe.close()
def va2off(va):
    r = va - IB
    for nm,rva,vs,pr,sr in secs:
        if rva <= r < rva + max(vs,sr): return pr + (r-rva)
    raise ValueError(hex(va))
def align(x,a): return (x + a - 1) & ~(a-1)

data = bytearray(open(DST,"rb").read())

# append new section ".cop"
new_rva  = align(LAST_RVA + LAST_VSZ, SA)
new_praw = align(len(data), FA)
SEC_RAW  = 0x1000
if len(data) < new_praw: data += b"\x00"*(new_praw-len(data))
data += b"\x00"*SEC_RAW
NEWBASE = IB + new_rva
opt = E_LFANEW + 4 + 20 + SIZE_OPT
sh = opt + NUM_SEC * 40
hdr = b".cop".ljust(8,b"\x00") + struct.pack("<IIII", SEC_RAW, new_rva, SEC_RAW, new_praw) + struct.pack("<IIHH",0,0,0,0) + struct.pack("<I",0xE0000060)
data[sh:sh+40] = hdr
struct.pack_into("<H", data, E_LFANEW+4+2, NUM_SEC+1)
struct.pack_into("<I", data, E_LFANEW+4+20+56, align(new_rva+SEC_RAW, SA))

cur = NEWBASE
def place_data(size, a=4):
    global cur; cur = align(cur,a); v=cur; cur+=size; return v
G_COUNT    = place_data(4)
G_CTRL     = place_data(4)
G_REGION   = place_data(4)
G_SINGLE   = place_data(4)
G_I        = place_data(4)
G_LASTCMD  = place_data(4)
G_LISTBUF  = place_data(0x20)   # output list object for the multi picker
G_OFFICERS = place_data(64*4)

def place_code(asm):
    global cur; cur = align(cur,4); va=cur
    b = bytes(ks.asm(asm, va)[0]); cur = va+len(b); return va,b

entry_asm = f"""
    mov dword ptr [0x{G_COUNT:X}], 0
    jmp 0x{DRIVER:X}
"""
# cave_pick: open the game's checkbox multi-select picker, read all checked officers
pick_asm = f"""
    mov dword ptr [0x{G_COUNT:X}], 0
    mov eax, dword ptr [esp+8]
    mov ecx, dword ptr [eax+0x18]
    mov dword ptr [0x{G_LISTBUF+0x18:X}], ecx
    mov ecx, dword ptr [eax+0x1C]
    mov dword ptr [0x{G_LISTBUF+0x1C:X}], ecx
    push 0
    push 1
    push 0x{COLS_TANSAKU:X}
    push 0x1F65
    push 0x40
    push eax
    push 0x{G_LISTBUF:X}
    call 0x{MULTI_PICK:X}
    add esp, 0x1C
    test eax, eax
    jz cpm_done
    mov edx, dword ptr [0x{G_LISTBUF+4:X}]
cpm_enum:
    test edx, edx
    jz cpm_disp
    mov eax, dword ptr [0x{G_COUNT:X}]
    cmp eax, 0x40
    jae cpm_disp
    mov ecx, dword ptr [edx+8]
    mov dword ptr [eax*4 + 0x{G_OFFICERS:X}], ecx
    inc eax
    mov dword ptr [0x{G_COUNT:X}], eax
    mov edx, dword ptr [edx]
    jmp cpm_enum
cpm_disp:
    mov eax, dword ptr [0x{G_COUNT:X}]
    test eax, eax
    jz cpm_done
    mov ecx, dword ptr [esp+4]
    mov edx, dword ptr [0x{G_OFFICERS:X}]
    mov dword ptr [ecx], edx
cpm_done:
    mov eax, dword ptr [0x{G_COUNT:X}]
    ret
"""
loop_asm = f"""
    mov eax, dword ptr [esp+4]
    mov dword ptr [0x{G_CTRL:X}], eax
    mov eax, dword ptr [esp+8]
    mov dword ptr [0x{G_REGION:X}], eax
    mov eax, dword ptr [esp+0xC]
    mov dword ptr [0x{G_SINGLE:X}], eax
    mov dword ptr [0x{G_LASTCMD:X}], 0
    cmp dword ptr [0x{G_COUNT:X}], 0
    jne multi
    push 0x44
    call 0x{NEW_OP:X}
    add esp, 4
    test eax, eax
    jz cl_ret
    push dword ptr [0x{G_REGION:X}]
    push dword ptr [0x{G_SINGLE:X}]
    push dword ptr [0x{G_CTRL:X}]
    mov ecx, eax
    call 0x{CMD_CTOR:X}
    mov dword ptr [0x{G_LASTCMD:X}], eax
    jmp cl_ret
multi:
    push 0x44
    call 0x{NEW_OP:X}
    add esp, 4
    test eax, eax
    jz cl_ret
    push dword ptr [0x{G_REGION:X}]
    push dword ptr [0x{G_OFFICERS:X}]
    push dword ptr [0x{G_CTRL:X}]
    mov ecx, eax
    call 0x{CMD_CTOR:X}
    mov dword ptr [0x{G_LASTCMD:X}], eax
    mov dword ptr [0x{G_I:X}], 1
aloop:
    mov eax, dword ptr [0x{G_I:X}]
    cmp eax, dword ptr [0x{G_COUNT:X}]
    jae cl_ret
    mov edx, dword ptr [0x{G_I:X}]
    push dword ptr [edx*4 + 0x{G_OFFICERS:X}]
    mov ecx, 0x{GLOBAL_OFFICERS:X}
    call 0x{APPEND_FN:X}
    inc dword ptr [0x{G_I:X}]
    jmp aloop
cl_ret:
    mov eax, dword ptr [0x{G_LASTCMD:X}]
    ret
"""
ENTRY_VA, ENTRY = place_code(entry_asm)
PICK_VA,  PICK  = place_code(pick_asm)
LOOP_VA,  LOOP  = place_code(loop_asm)

# cave_execute: run the command's execute once per officer in the global list
exec_asm = f"""
    push esi
    push edi
    mov esi, ecx
    xor edi, edi
xloop:
    mov ecx, esi
    call 0x{EXEC_ORIG:X}
    mov eax, dword ptr [0x{GLOBAL_OFFICERS+4:X}]
    test eax, eax
    jz xdone
    mov edx, dword ptr [eax]
    mov dword ptr [0x{GLOBAL_OFFICERS+4:X}], edx
    test edx, edx
    jz xdone
    inc edi
    cmp edi, 0x40
    jae xdone
    jmp xloop
xdone:
    pop edi
    pop esi
    ret
"""
EXEC_VA, EXEC = place_code(exec_asm)

def write_new(va,b):
    o = new_praw + (va - NEWBASE); data[o:o+len(b)] = b
for va,b in ((ENTRY_VA,ENTRY),(PICK_VA,PICK),(LOOP_VA,LOOP),(EXEC_VA,EXEC)):
    write_new(va,b)

# patches
struct.pack_into("<I", data, va2off(VT_SLOT), ENTRY_VA)
# redirect 探索 command execute (vtable[11]) to the per-officer loop
assert struct.unpack_from("<I", data, va2off(VT_EXEC))[0] == EXEC_ORIG, "VT_EXEC slot mismatch"
struct.pack_into("<I", data, va2off(VT_EXEC), EXEC_VA)
c=bytes(ks.asm(f"call 0x{PICK_VA:X}", SITE_PICK)[0]); data[va2off(SITE_PICK):va2off(SITE_PICK)+5]=c
# flip 探索 officer-list control type single(0x1E)->multi(0x1C)  (byte after opcode 0x6A)
assert data[va2off(SITE_CTRLTYPE):va2off(SITE_CTRLTYPE)+2] == b"\x6A\x1E", data[va2off(SITE_CTRLTYPE):va2off(SITE_CTRLTYPE)+2].hex()
data[va2off(SITE_CTRLTYPE)+1] = 0x1C
drv_asm = f"""
    mov byte ptr [esp+0xEEC], 1
    mov eax, dword ptr [esp+0x6B4]
    mov edx, dword ptr [esp+0x6B8]
    push eax
    push edx
    push esi
    call 0x{LOOP_VA:X}
    add esp, 0x0C
    mov esi, eax
    jmp 0x{DRV_CONT:X}
"""
c=bytes(ks.asm(drv_asm, SITE_DRV)[0]); assert len(c)<=0x38; c=c+b"\x90"*(0x38-len(c))
data[va2off(SITE_DRV):va2off(SITE_DRV)+0x38]=c

open(DST,"wb").write(data)
print("Wrote",DST,"size",len(data))
print("  G_COUNT=0x%08X G_OFFICERS=0x%08X"%(G_COUNT,G_OFFICERS))
for nm,va in (("tansaku_entry",ENTRY_VA),("cave_pick",PICK_VA),("create_loop",LOOP_VA),("cave_execute",EXEC_VA)):
    print("  %-15s @ 0x%08X"%(nm,va))
