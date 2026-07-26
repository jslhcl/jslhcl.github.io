# Task: Multi-officer 探索 (search) command for San9PK (RTK9 PK, TC build)

## Goal
Modify `San9PK.exe` so the 探索 (search) command lets the player pick MANY officers per
command instead of one. Output as `San9PK_copilot.exe` in the game folder. Back up any file
we overwrite.

## Key facts
- Game: `C:\Program Files (x86)\Koei\San9 Tc\San9PK.exe`, x86 PE, ImageBase 0x400000.
- .text: RVA 0x1000, file off 0x400. file_off -> RVA = +0xC00 ; VA = file_off + 0x400C00.
- Last section .mackt ends at EOF => a code cave requires appending a new PE section.
- Community "multi-officer" mods redirect a `call` (E8 rel32) per command to an appended
  code-cave handler. Their byte offsets are for a DIFFERENT build (don't match ours).
- Binary retains MFC CRuntimeClass name strings. Anchor class: **COrderTansakuDlg**
  (the 探索 order dialog). Related: CBushouMessageDlg, CSelectDlg, CSan9ListDlg,
  CCommandMenuDlg, CSelectMapObjectDlg, CMakeNewBushouDlg, CForceMenuDlg.

## Approach (subject to findings)
1. Resolve COrderTansakuDlg CRuntimeClass -> methods / message map.
2. Identify button handlers: 執行武將 (select officer) and 執行 (execute), plus where the
   single selected officer id is stored and how the command is committed.
3. Design multi-select: reuse an existing multi-officer select list if one exists, OR loop.
4. Implement via appended code-cave section + call redirect. Write San9PK_copilot.exe only.
5. User tests in-game (I cannot play through to verify).

## REVISED GOAL (user clarification 2026-07-25)
User wants: 探索 dialog -> click 執行武将 -> the officer LIST itself allows selecting
MULTIPLE officers (multi-pick), then all selected get a search order. NOT a loop of the
whole dialog. My previous "loop driver" patch (vtable 0x609FC0 -> cave) was wrong UX; rebuild
fresh from original.

## Officer picker chain
- 執行武将 button handler = COrderTansakuDlg::OnCmd 0x4EC310, branch id 0x3E9 (0x4EC3F3..).
  calls `0x570380(list=&[dlg+0xED4], ctrl=&[dlg+0x6B4], 0x1F65, 0x66C694, 0,0)`.
- 0x570380 -> prepends mode 0x0A -> 0x56F930 (core list dialog). Creates dialog via 0x56EA20,
  DoModal [vt+0x80], extracts ONE result via 0x572810 -> stores single id to output [ebp].
- Selected officer stored at [dlg+0xED4]; region at [dlg+0xED8].
- 執行 handler 0x4EB650: officer=[dlg+0xED4] -> [dlg+0x6AC]; region=[dlg+0xED8]->[dlg+0x6B0];
  jmp 0x4CB480 (close). Driver 0x4C6C90 then new(0x44)+0x493EA0(controller,officer,region)=1 order.

## CONFIRMED (user 2026-07-25): officer list is NATIVELY multi-select (can highlight several
## + confirm). 探索 just keeps the FIRST selected. FIX = capture all selected + 1 order each.

## Selection internals
- List dialog selection set @[dlg+0x154]; item pairs {value,flags}. Multi-enumerator 0x572810
  (this=dlg, arg1=out list, arg2=mode). mode 1..3 -> append site 0x57286B (per selected item);
  mode 4 -> 0x57288E (all). 0x572810 has 57 callers (shared) -> must gate capture.
- 0x56F930 harvests officer pick via 0x572810(mode1) @0x56FA5C, keeps only first ([node+8]).
- Officer id captured = value from 0x56A6C0 = same id original single path uses.

## ATTEMPT 3 RESULT: picker reopen works (multi-pick confirmed live); 執行 CRASHES in create.
## Full-dword fix didn't help. Root issue: creating N 探索 command objects in a tight loop.

## USER wants CHECKBOX multi-select (screenshot): the 訓練 (Training)=COrderKunrenDlg picker.
## Findings:
## - Multi picker = 0x570500 -> core 0x570150 (fills an OUTPUT LIST via 0x572810 mode1 w/ ALL
##   checked officers). Single picker = 0x570380 -> 0x56F930 (keeps only first).
## - Kunren OnCommand 0x4DF8E0 (btn 0x3E8) -> 0x4DF880 calls 0x570500(out=&[dlg+0x6EC],
##   ctrl=&[dlg+0x6CC], max, 0x1F65, cols=0x66C658, 1, 0); process via 0x46F610.
## - Kunren EXECUTE 0x4E6C80: copies officer LIST [dlg+0x6EC]->[dlg+0x6AC], jmp 0x4CB480.
##   Kunren driver 0x4C37A0: new(0x40); 0x489D80(cmd, controller, &officerLIST). ONE cmd, list.
## - Tansaku cmd ctor 0x493EA0: new(0x44); scalar officer+region. Base ctor chain touches global
##   scratch list 0x15455AC (cleared+append per construction) -> shared, so tight-loop N unsafe.
## - Tansaku cmd vtable 0x608528; Kunren cmd vtable 0x607C38 (type 5).

## OPEN QUESTION for fix direction: does 探索 crash with just ONE picked officer? (isolates
## create_loop core bug vs multi-creation/global-scratch). Then either (a) one-cmd-with-list like
## 訓練 if 探索 exec iterates officer list, or (b) find correct per-order registration.

## ATTEMPT: EXECUTE-LOOP (2026-07-25) — double-check confirmed + fix
## VERIFIED the user's suspicion by static RE:
##  - 探索 cmd execute = 0x493F90 (vtable[11] slot 0x608554). It calls 0x4922E0->0x492F50
##    FIRST, which ITERATES the whole 0x15455AC list and does 0x44C8A0(officer,0x1000,1) =
##    set [officer+0xE8] |= 0x1000 (the BUSY flag) on EVERY node. THEN 0x493F90 reads only the
##    HEAD officer (0x485E50 -> [0x15455B0]=[list+4]=head node -> [+8]=officer) and builds ONE
##    search unit (0x485AA0) + one counsellor msg (0x1625). => all officers busy, one searches.
##  - Because busy-marking iterates the FULL list AT EXECUTE and v3 marks all busy, 0x15455AC
##    provably holds ALL officers at execute time. So the fix: loop execute per officer.
## FIX: new cave_execute (0x1B59298), vtable[11] slot 0x608554 -> cave_execute. It repeatedly
##  calls 0x493F90 then pops the head ([0x15455B0]=[eax]) until empty (cap 0x40) => one search
##  unit per officer. vtable[8]/cave_pick/create_loop unchanged.
## BUILD SHA256 3E489598A9773DD53B4BCCE54250385C90063F0B21B3B6E48D10661EDE94D872 (2,640,896 B).
## Status: awaiting user in-game test (expect all selected officers to actually search now).


## Switch to GUARANTEED accumulate: cave_pick loops the single picker, capturing each pick
## from *output(&ed4), until cancel. Self-diagnosing: list REOPENS after each pick if active.

## ATTEMPT 3 design (rebuild fresh from original)
Data in .cop: g_count(dword), g_officers[64] words.
Caves:
 - tansaku_entry: g_count=0; jmp 0x4C6C90
 - cave_pick (replaces call@0x4EC414): g_count=0; loop{ forward 6 args->call 0x570380;
     if eax==0 break; ax=*[output=arg1]; g_officers[g_count++]=ax (cap 0x40) }; eax=g_count; ret
 - create_loop (driver 0x4C6D04 block): if g_count>0 loop new(0x44)+0x493EA0(ctrl,g_off[i],region)
     else single fallback [dlg+0x6AC]; return last.
Patches: 1) vtable 0x609FC0->tansaku_entry  2) call@0x4EC414->cave_pick
         5) driver block 0x4C6D04..0x4C6D3C -> call create_loop; jmp 0x4C6D3C
(Drop mode1_hook & record_officer hooks from attempt 2.)
Diagnostic: if picker reopens after each pick => patches active.

Data: g_count(dword), g_capture(dword), g_officers[64] (words).
Caves:
 - tansaku_entry: g_count=0; g_capture=0; jmp 0x4C6C90   (reset per 探索 command)
 - cave_pick: g_capture=1; forward 6 args -> call 0x570380; g_capture=0; ret  (isolate capture)
 - mode1_hook: if g_capture: g_count=0; mov eax,1; jmp 0x572844  (reset each mode1..3 enum)
 - record_officer: if g_capture & room: g_officers[g_count++]=ax; jmp 0x46EF70 (append hook)
 - create_loop: if g_count>0 loop new(0x44)+0x493EA0(controller,g_officers[i],region);
                else single fallback with [dlg+0x6AC]. returns last.
Patches:
 1) vtable slot 0x609FC0 -> tansaku_entry
 2) call@0x4EC414 (0x570380) -> cave_pick
 3) mov eax,1 @0x57283F -> jmp mode1_hook
 4) call@0x57286B (0x46EF70) -> record_officer
 5) driver create block 0x4C6D04..0x4C6D3C -> (set SEH; push single,region,controller;
    call create_loop; add esp,0xC; mov esi,eax; jmp 0x4C6D3C)
Rebuild fresh from original San9PK.exe (drop earlier loop patch). Use keystone to assemble.


- 探索 command handler object vtable = 0x609FA0 (array of per-command vtables, stride 0x30).
  Slot [8] (offset +0x20) at VA 0x609FC0 (file 0x2091C0) = driver 0x4C6C90.
- Driver 0x4C6C90 (__thiscall, ecx=controller, `ret` no-imm, return discarded by caller):
  construct COrderTansakuDlg -> DoModal(0x41FB00) -> if result==1: new(0x44)+0x493EA0(
  controller, officer[dlg+0x6AC], region[dlg+0x6B0]) which REGISTERS the order (ctor touches
  global mgr 0x15455AC; dispatcher at 0x50F54B discards return) -> destruct -> return cmd/0.
- PATCH: point vtable slot 0x609FC0 -> code cave `loop_tansaku` that loops calling 0x4C6C90
  until it returns 0 (user clicked 中止/Cancel). Each iteration = one full search session that
  registers one searcher. Only affects 探索.
- Cave (~21 bytes): push esi; mov esi,ecx; L: push 0; mov ecx,esi; call 0x4C6C90; add esp,4;
  test eax,eax; jnz L; pop esi; ret.
- Output: San9PK_copilot.exe (copy). Original untouched.

## Status
- [x] Recon: PE layout, imports, strings, community mechanism.
- [x] Resolve COrderTansakuDlg MFC metadata + handlers (vtable 0x60D0F0, Execute 0x4EB650).
- [x] Understand single-officer execute/commit + registration path.
- [x] Design patch (vtable redirect + loop cave).
- [ ] Find/allocate code cave; write San9PK_copilot.exe.
- [ ] User validation in-game (I cannot play-test).

## NOTE: unverified binary mod -> needs user in-game testing; iterate if needed.
## Research agent rtk9-mod-research: idle (confirmed no public 探索 static patch; TC build unique).
