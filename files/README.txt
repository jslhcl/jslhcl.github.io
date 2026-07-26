San9PK — Multi-officer 探索 (Search) mod
=========================================

WHAT THIS DOES
  Patches "San9 with Power-Up Kit" (三國志IX PK, Traditional Chinese build) so the
  探索 (Search) command lets you pick MANY officers at once (checkbox picker), and
  EVERY selected officer actually performs their own search that round.

  The original San9PK.exe is NEVER modified. The patcher writes a new copy named
  San9PK_copilot.exe with an extra PE section (".cop") that holds a few data buffers
  and small hand-assembled code caves; a handful of instructions / vtable slots in
  the copy are redirected into those caves.


FILES IN THIS FOLDER
  patch3.py            THE build script. Reads a pristine San9PK.exe and produces
                       San9PK_copilot.exe. This is the one file you truly must keep.
  San9PK.original.exe  A pristine, UNMODIFIED copy of the game exe (the build source).
                       Keep it — patch3.py needs a clean exe to patch.
  San9PK_copilot.exe   The finished, working patched game (ready to use).
  plan.md              Full reverse-engineering notes: every address, why each patch
                       exists, and the history of the fix. Read this to understand or
                       extend the mod later.
  an.py / an2.py / an3.py
                       Small reverse-engineering helper scripts (disassemble, dump,
                       find cross-references). Not needed to build; useful if you ever
                       want to investigate the exe further. Main one is an2.py.


WORKING BUILD FINGERPRINT
  San9PK_copilot.exe
  Size   : 2,640,896 bytes
  SHA256 : 3E489598A9773DD53B4BCCE54250385C90063F0B21B3B6E48D10661EDE94D872
  (Verify with:  Get-FileHash .\San9PK_copilot.exe -Algorithm SHA256 )


HOW TO INSTALL
  Copy San9PK_copilot.exe into the game folder:
      C:\Program Files (x86)\Koei\San9 Tc\
  (Writing there needs administrator rights.) Launch San9PK_copilot.exe.
  Your original San9PK.exe stays untouched, so you can always fall back to it.


HOW TO REBUILD FROM SCRATCH (if you lose San9PK_copilot.exe)
  1. Install Python 3 (any recent 3.x).
  2. Install the three build libraries:
         pip install capstone pefile keystone-engine
  3. Make sure patch3.py points SRC at a pristine exe. By default it is:
         SRC = r"C:\Program Files (x86)\Koei\San9 Tc\San9PK.exe"
     If that copy might be modified, edit the SRC line at the top of patch3.py to
     point at San9PK.original.exe instead, e.g.:
         SRC = r"C:\Users\leca\Desktop\San9PK_multiofficer_mod\San9PK.original.exe"
  4. Build:
         python patch3.py ".\San9PK_copilot.exe"
     It prints the new section layout and cave addresses, and self-verifies the
     patch points with assertions. Confirm the SHA256 matches the fingerprint above.
  5. Install as described in "HOW TO INSTALL".

  IMPORTANT: patch3.py must always build from a PRISTINE exe. Never point SRC at an
  already-patched San9PK_copilot.exe, or you'll stack patches and corrupt it.


WHAT THE PATCH CHANGES (summary — full detail in plan.md)
  * Appends a new ".cop" PE section (writable + executable) for data + code caves.
  * Officer-list control type flipped single(0x1E) -> multi(0x1C) so the 執行武将
    list shows checkboxes (the 訓練/Training-style multi picker, func 0x570500).
  * cave_pick captures every checked officer into a buffer.
  * create_loop builds the 探索 command and puts all picked officers into the
    global officer list 0x15455AC.
  * cave_execute (vtable[11] slot 0x608554 of the 探索 command) re-runs the original
    execute 0x493F90 once per officer in the list, so each officer gets their own
    search unit. (Note: you now get one counsellor search hint per officer.)
