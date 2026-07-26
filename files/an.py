import pefile, sys, struct, collections

PATH = r"C:\Program Files (x86)\Koei\San9 Tc\San9PK.exe"
pe = pefile.PE(PATH)
IB = pe.OPTIONAL_HEADER.ImageBase
data = pe.__data__  # full file bytes

# section map
SECS = []
for s in pe.sections:
    SECS.append((s.Name.rstrip(b"\x00").decode(errors="replace"),
                 s.VirtualAddress, s.Misc_VirtualSize, s.PointerToRawData, s.SizeOfRawData))

def rva_to_off(rva):
    for name,va,vs,praw,sraw in SECS:
        if va <= rva < va+max(vs,sraw):
            if rva-va < sraw:
                return praw + (rva-va)
    return None

def off_to_rva(off):
    for name,va,vs,praw,sraw in SECS:
        if praw <= off < praw+sraw:
            return va + (off-praw)
    return None

def va_to_off(va):
    return rva_to_off(va-IB)

def off_to_va(off):
    r = off_to_rva(off)
    return IB+r if r is not None else None

# .text bounds
TEXT = [s for s in SECS if s[0]==".text"][0]
tname,tva,tvs,tpraw,tsraw = TEXT
text_start_off = tpraw
text_end_off = tpraw + tsraw
text_start_va = IB + tva
text_end_va = IB + tva + tvs

def scan_calls():
    """Scan for E8 rel32 direct calls; return dict target_va -> list of call_site_va"""
    targets = collections.defaultdict(list)
    b = data
    i = text_start_off
    end = text_end_off
    while i < end-5:
        if b[i]==0xE8:
            rel = struct.unpack_from("<i", b, i+1)[0]
            site_va = off_to_va(i)
            tgt = site_va + 5 + rel
            if text_start_va <= tgt < text_end_va:
                targets[tgt].append(site_va)
            i += 5
        else:
            i += 1
    return targets

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv)>1 else "hot"
    if cmd=="hot":
        t = scan_calls()
        items = sorted(t.items(), key=lambda kv: -len(kv[1]))
        print("Top called functions (target_va : callers):")
        for va,callers in items[:40]:
            print("  0x%08X  x%d" % (va, len(callers)))
    elif cmd=="callers":
        want = int(sys.argv[2],16)
        t = scan_calls()
        callers = sorted(t.get(want,[]))
        print("Callers of 0x%08X (%d):" % (want, len(callers)))
        for c in callers:
            print("  0x%08X (off 0x%X)" % (c, va_to_off(c)))
