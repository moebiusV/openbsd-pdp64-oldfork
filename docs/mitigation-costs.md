# OpenBSD policies and mitigations: cost on pdp64

OpenBSD base: master `c402c876540c` (2026-11-24, 8.0-current; 8.0 released 2026-10-20). Branch `pdp64`. Written 2026-11-24 from the GitHub mirror and checked against the checkout.


Verdicts: **gone** (code not needed), **cheaper**, **same**, **worse**. "Needs" = prerequisite from §1.

| OpenBSD policy / mitigation | Cost on amd64 / arm64 / riscv64 today | On pdp64 | Verdict | Needs |
|---|---|---|---|---|
| Meltdown: separate user/kernel page tables, `.kutext` trampoline, `cr3` switch each entry | amd64: trampoline page + 2 `cr3` writes per syscall | user mode never walks `KTBR`; mode change selects the half in hardware; no trampoline, no flush | **gone** | A4, Q2 |
| Kernel entry: stack switch, `swapgs`/`sscratch`↔`tp` swap, saving state the CPU pushed | riscv64 swaps `tp`/`sp` via `sscratch`; amd64 `swapgs` + lfence | banked `R14` and `DP`: kernel stack and `curcpu()` are already there; entry writes 4 registers and cannot fault; `PUSHX` saves `EPC`+`EPSW` in one instruction | **cheaper** (est. 4–5 instructions to C) | — |
| `curcpu()` | `%gs:` / `tpidr_el1` / `tp` | `MOVQ d(DP),Rd`, never needs re-establishing | **cheaper** | `d(DP)` store form (J.9.5) |
| SMAP/PAN/SUM around copyin/copyout; boot-time `stac`/`clac` patching | amd64: codepatch (17 tags, 75 refs, `codepatch.c`) | `UA` is architectural and cleared on every entry; `.U` moves do the access with user rights and need no window at all | **gone** (patching), **cheaper** (guard) | J.6.12 |
| `codepatch` / CPU-variant selection (retpoline, MDS `verw`, IBPB, IBRS, xsave variants) | amd64 `cpu.c`+`identcpu.c` ≈ 2,650 lines | one uniform core, no microcode, no variant table | **gone** | — |
| Spectre-class: retpolines, RSB stuffing, `lfence` after `swapgs`, BHB clear, MDS buffer clear | per-entry and per-indirect-call cost | spec is "OoO-ready: nothing is safe only because the core does not speculate"; `HINT #2` barrier exists; predictor isolation by ASID approved | **gone today**; revisit when an OoO core exists | — |
| SMT disabled by default (`hw.smt`) | half the logical CPUs off | no SMT | **gone** | — |
| FPU: eager save/restore, `xsave` area, FPU-disabled traps | arm64/riscv64 save 32 FP regs + lazy-enable trap | FP lives in the GPRs; state is 5 sticky bits in `FPSR`; vector blocks keep **no** state across a switch (restart at `VEC`) | **gone** (FPU code), but trapframe is 32 GPRs | A7, A14 |
| TLB shootdown IPIs in pmap | `pmap_tlb_shoot*` + IPI handlers on every MP port | `TLBI` broadcasts in hardware, `TLBSYNC` waits: unmap is 3 lines | **gone** | Q2 |
| ASID/PCID handling | amd64 PCID juggling with Meltdown | 16-bit ASID; switch = `PTBR`+`ASID`+`ISYNC`, no flush | **cheaper** | Q2 |
| Execute-only (xonly) text | amd64 only via PKU; kernel copyin checks elsewhere | PTE `R=0,X=1` is ordinary; fetch vs read faults are different vectors (9 vs 10); `UA` makes kernel reads of user text fault too | **cheaper** — but the compiler must stop putting pools/tables in `.text` | A8, T5 |
| W^X (user and kernel) | policy over PTE bits | same; separate `R W X`, kernel can never execute `U` pages; kernel text needs 2 MB/4 KB leaves, not 1 GB | **same** (native) | — |
| PIE / static-PIE / ASLR | small on amd64/arm64 | PC-relative is the *shorter* encoding, so PIE costs nothing in size; **but** 39-bit VA gives a 38-bit user half: ~26 bits of page entropy vs 35 on amd64 | **cheaper** in code, **worse** in entropy | 4-level walk (not implemented) |
| KARL, libc/ld.so/sshd random relink | boot-time link | PC-relative code relinks without runtime relocation | **same** (needs lld `-r` + script) | T3 |
| pinsyscalls | table lookup keyed by PC at entry | `EPC` is a register (no stack fetch); check ≈ 4 instructions; `SYS` page bit would give the region check for free | **cheaper** | A2, A10 |
| `MAP_STACK` stack-pointer check at syscall/fault | read saved SP from frame | `MFSR usp` — one instruction, entry cannot fault | **cheaper** | — |
| Landing pads (BTI/IBT) | `endbr64`/`bti c` everywhere, per-page guard on arm64 | `LPAD` (2 bytes) only on address-taken functions; vector 14; enforcement switch not yet assigned | **same**, pending A10 | A10 |
| Retguard | amd64 2+3 instructions/function; arm64 3+5; riscv64 unsupported | return address is on the data stack (no link register) → same exposure as amd64; check can be one `ct` instruction, no int3 sled | **same** (slightly smaller) | T8 |
| ROP-gadget reduction (`X86FixupGadgets`, register-order tricks) | amd64-only compiler passes | instructions are 16-bit-parcel aligned: a hidden `RET` can exist only at parcel offsets, and xonly rule keeps data out of text | **cheaper** (pass likely unnecessary — measure) | — |
| `-fret-clean` | 1 store per return (amd64) | same shape | **same** | T8 |
| Stack protector | canary load/compare | same | **same** | — |
| Trap sleds / `int3` padding between functions | padding bytes | `HALT`/illegal parcel padding; same idea | **same** | — |
| Memory barriers, publication races (e.g. the 2025 pinsyscalls table race) | `membar_*` on arm64/riscv64/powerpc | memory model is sequentially consistent: barriers are empty and that bug class does not exist | **gone** | — |
| copyin/copyout/copyinstr, `pagezero`, `memcpy`/`memset`/`strlen` asm | 100s of lines per port, fault-recovery via `pcb_onfault` | `MCPY`/`MSET`/`MSCN` are single restartable instructions; with `.U`/`UA` a copy routine is ~6 instructions | **cheaper** (asm nearly vanishes) | — |
| Page-fault restart, A/D emulation | arch-specific fixups | every fault is precise and blindly restartable; A/D are software-managed exactly as riscv64's pmap already does | **same as riscv64** (reuse) | — |
| `KASSERT`/`panic` sites, `-ftrapv`, bounds checks | call + string per site | `ct<cc>`/`chk2`/`TRAPCC`/`ADDV` + 12-byte `__bug_table` record, vector 16 | **cheaper** | vector-16 handler (handoff §7.7) |
| DMA attacks / device isolation | VT-d/SMMU drivers optional | IOMMU is part of the platform, blocked at reset | **cheaper** (on by default) | Q4 |
| Return-to-user register hygiene | — | hole 6: kernel `r2`–`r13` visible after `RTI` unless scrubbed; hole 7: `FPSR` leaks | **worse until decided** | A14 |
| sigreturn cookie, setjmp cookie, `mimmutable`, `pledge`, `unveil`, `kbind`, malloc hardening | MI or libc | unchanged (`MSET` helps junk-fill; broadcast `TLBI` helps unmap-on-free) | **same** | — |

`pdp64/docs/openbsd-mitigations.md` (2026-10-22) is the earlier study; several of its claims are
stale against the current design (it says "no FPU state", "no speculation", lists `RDTIME`/feature
registers as pending). The new table supersedes its summary and will cite manual sections.

---
