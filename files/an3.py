import an2, struct
data=an2.data
# find callers of 0x56f930 (E8 rel32)
target=0x56f930
print("=== callers of 0x56F930 (core selector) and preceding pushed mode ===")
i=an2.SECS[0][3]; end=i+an2.SECS[0][4]
b=data
while i<end-5:
    if b[i]==0xE8:
        rel=struct.unpack_from("<i",b,i+1)[0]
        site=an2.off_to_va(i)
        if site+5+rel==target:
            # look back up to 0x20 bytes for a push imm8/imm32 that is the mode (first arg)
            # crude: disassemble 0x30 bytes before
            start=i-0x30
            code=b[start:i+5]
            # find last 'push' near call by scanning; just print raw context via capstone
            print("caller call@0x%08X"%site)
        i+=5
    else:
        i+=1

print()
print("=== also callers of wrapper 0x570380 (mode 0x0A single) ===")
target=0x570380
i=an2.SECS[0][3]
while i<end-5:
    if b[i]==0xE8:
        rel=struct.unpack_from("<i",b,i+1)[0]
        site=an2.off_to_va(i)
        if site+5+rel==target:
            print("caller call@0x%08X"%site)
        i+=5
    else:
        i+=1

print()
print("=== occurrences of imm 0x0ED4 and 0x0ED8 in .text (mov r,[reg+0xED4]) ===")
for label,imm in (("ED4",0x0ED4),("ED8",0x0ED8)):
    needle=struct.pack("<I",imm)  # 0x00000ED4 little-endian D4 0E 00 00
    pos=an2.SECS[0][3]; cnt=0
    while True:
        p=data.find(needle,pos, end)
        if p<0: break
        va=an2.off_to_va(p)
        print("  imm 0x%s ref@disp in insn near VA 0x%08X (file0x%X)"%(label, va, p))
        pos=p+1; cnt+=1
        if cnt>40: break
