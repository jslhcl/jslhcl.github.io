import pefile, struct, sys, collections
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

PATH = r"C:\Program Files (x86)\Koei\San9 Tc\San9PK.exe"
pe = pefile.PE(PATH)
IB = pe.OPTIONAL_HEADER.ImageBase
data = pe.__data__
SECS=[]
for s in pe.sections:
    SECS.append((s.Name.rstrip(b"\x00").decode(errors="replace"),s.VirtualAddress,s.Misc_VirtualSize,s.PointerToRawData,s.SizeOfRawData))
md = Cs(CS_ARCH_X86, CS_MODE_32)
md.detail = True

def off_to_va(off):
    for n,va,vs,pr,sr in SECS:
        if pr<=off<pr+sr: return IB+va+(off-pr)
    return None
def va_to_off(va):
    r=va-IB
    for n,va2,vs,pr,sr in SECS:
        if va2<=r<va2+sr: return pr+(r-va2)
    return None
def secname(va):
    r=va-IB
    for n,va2,vs,pr,sr in SECS:
        if va2<=r<va2+max(vs,sr): return n
    return "?"

def read(va, n):
    o=va_to_off(va)
    if o is None: return None
    return data[o:o+n]

def u32(va):
    b=read(va,4)
    return struct.unpack("<I",b)[0] if b else None

def dump(va, n=0x40):
    print("dump 0x%08X (%s):" % (va, secname(va)))
    o=va_to_off(va)
    b=data[o:o+n]
    for i in range(0,len(b),16):
        chunk=b[i:i+16]
        hexs=" ".join("%02X"%c for c in chunk)
        # interpret 4-byte words
        words=""
        if i+16<=len(b):
            ws=struct.unpack("<4I", chunk)
            words=" ".join("%08X"%w for w in ws)
        asc="".join(chr(c) if 32<=c<127 else "." for c in chunk)
        print("  +%03X %-47s |%-16s| %s"%(i,hexs,asc,words))

TEXT=[s for s in SECS if s[0]==".text"][0]
tva=TEXT[1]; tvs=TEXT[2]; tpr=TEXT[3]; tsr=TEXT[4]

def find_imm_refs(va):
    """find 4-byte little-endian occurrences of va across whole file, report VA of location"""
    needle=struct.pack("<I",va)
    hits=[]; pos=0
    while True:
        p=data.find(needle,pos)
        if p<0: break
        loc=off_to_va(p)
        hits.append((p,loc))
        pos=p+1
    return hits

def disasm(va, n=0x60, count=None):
    o=va_to_off(va)
    b=data[o:o+n]
    k=0
    for ins in md.disasm(b, va):
        print("  0x%08X  %-22s %s %s"%(ins.address," ".join("%02X"%c for c in ins.bytes), ins.mnemonic, ins.op_str))
        k+=1
        if count and k>=count: break

if __name__=="__main__":
    cmd=sys.argv[1]
    if cmd=="dump":
        dump(int(sys.argv[2],16), int(sys.argv[3],16) if len(sys.argv)>3 else 0x40)
    elif cmd=="refs":
        va=int(sys.argv[2],16)
        for off,loc in find_imm_refs(va):
            print("ref@0x%08X (%s) file0x%X"%(loc,secname(loc),off))
    elif cmd=="dis":
        disasm(int(sys.argv[2],16), int(sys.argv[3],16) if len(sys.argv)>3 else 0x80)
    elif cmd=="u32":
        print("0x%08X"%u32(int(sys.argv[2],16)))
