# Assembly translation verdicts (riscv64 template)

OpenBSD base: master `c402c876540c` (2026-11-24, 8.0-current; 8.0 released 2026-10-20). Branch `pdp64`. Written 2026-11-24 from the GitHub mirror and checked against the checkout.


Template: the **riscv64** port — newest, smallest, same shape (LP64 LE, software A/D bits, 16-bit
ASID, Sv39-style tables; the pdp64 PTE low byte `V R W X U G A D` is bit-for-bit riscv64's). Sizes
are from OpenBSD master `c402c876` (2026-11-24) via the GitHub mirror; the checkout step regenerates
this table by script so it is exact. Verdicts: **T** translate, **1** collapses to one or a few
pdp64 instructions, **D** delete (no pdp64 equivalent needed), **N** new (no riscv64 counterpart).

### 2a. Kernel — `sys/arch/riscv64/riscv64/` (8 files, 1,082 lines)

| File | Lines | What it holds | pdp64 verdict | Blocked on |
|---|---:|---|---|---|
| `locore0.S` | 47 | `_start`, linked first (KARL fixes only this) | **T** — entry from `-kernel`/loader, boot-info pointer | Q3 |
| `locore.S` | 268 | bootstrap page tables, MMU on, `stvec`, initstack, `sigcode`/`sigcoderet`/`sigfill`, `cpu_hatch` | **T** — `MTSR vbr/ptbr/ktbr/mmuctl` + `ISYNC`; a 4 KB vector table (512 quads) replaces `stvec`; sigcode is `TRAP` + filler | A2, A4, A11 |
| `exception.S` | 244 | save/restore 31 regs, user/kernel entry split, `sscratch`↔`tp` swap, SUM clear, AST, `syscall_return` | **T, shrinks** — no stack/`tp` swap (banked `R14`/`DP`), no SUM clear (entry clears `UA`), `PUSHX`/`POPX`; still saves 32 GPRs + `USP` + `FPSR`; separate vectors per cause remove the dispatch | A7, A14 |
| `cpuswitch.S` | 99 | `cpu_switchto_asm`, `proc_trampoline` | **T** — callee-saved set + `USP` + user `DP`; `PTBR`+`ASID`+`ISYNC` | A3, A7 |
| `copy.S` | 177 | `copyin`, `copyin32`, `copyout`, `kcopy` with `pcb_onfault`, SUM window | **1** — bounds check + `MCPY` with `.U`/`UA`; fault fixup via table or `pcb_onfault` | J.6.12 |
| `copystr.S` | 116 | `copyinstr`, `copyoutstr` | **1** — `MSCN` for the NUL + `MCPY` | J.6.12 |
| `support.S` | 89 | kernel `setjmp`/`longjmp` (ddb) | **T** | A7 |
| `pagezero.S` | 42 | `pagezero` | **1** — one `MSET` | — |
| `genassym.cf` | 72 | struct offsets | **T** | — |
| (arm64 only) `trampoline.S` 220, `cpufunc_asm.S` 253, `lse.S` 170 | | Meltdown trampoline, TLB/cache ops, out-of-line atomics | **D** — `KTBR` split, `TLBI`/`ICINV` are single instructions, atomics inline | — |
| `stand/efiboot/start.S` | 170 | PE/COFF header for the UEFI loader | **D for first boot** (`-kernel`); a block-0 loader comes later | — |
| — | | vector-16 check handler + `__bug_table` walker | **N** | handoff §7.7 |

There is no `sys/lib/libkern/arch/riscv64` (string routines are C) and no mutex asm — pdp64 may add
`MCPY`/`MSET`/`MSCN` one-liners there as an optimisation, not a requirement.

**Headers with asm macros / inline asm** (`sys/arch/riscv64/include/`, 50 files): `asm.h`
(`ENTRY`/`END`, `RETGUARD_*`, user-access macros), `cpu.h` (`curcpu()` via `tp` → `d(DP)`),
`atomic.h`, `cpufunc.h`, `riscvreg.h` (CSR accessors → `MFSR`/`MTSR` intrinsics), `profile.h`
(`_mcount`), `sbi.h` (**D**). The ~40 structural/ABI headers (`frame.h`, `pcb.h`, `pte.h`, `pmap.h`,
`param.h`, `vmparam.h`, `_types.h`, `signal.h`, `reg.h`, `tcb.h`, `reloc.h`, `fenv.h`…) are
rewritten, not translated.

### 2b. Userland assembly

| Path | Files / lines | Content | Verdict | Blocked on |
|---|---|---|---|---|
| `lib/libc/arch/riscv64/SYS.h`, `DEFS.h` | 198 | syscall stub macros, `PINSYSCALL` records into `.openbsd.syscalls` | **T** — stub is `TRAP` + error branch | A2 |
| `lib/libc/arch/riscv64/sys/*.S` | 8 / 375 | `Ovfork`, `brk`, `sbrk`, `sigpending`, `sigprocmask`, `sigsuspend`, `syscall`, `tfork_thread` | **T** | A2 |
| `lib/libc/arch/riscv64/gen/{_setjmp,setjmp,sigsetjmp}.S` | 3 / 376 | setjmp family | **T** — plus `__jmpxor` mangling of SP and the return slot | A7 |
| `lib/libc/arch/riscv64/gen/_atomic_lock.c`, `fp*.c`, `fabs.c`, `flt_rounds.c` | ~16 C files w/ inline asm | spinlock, FP mode/flags | **T** — `SWAP`; `FPSR` has flags only, no rounding-mode/mask bits, so most `fpset*` become trivial | A1 |
| `lib/csu/riscv64/md_init.h` | 112 | `_start`, static-PIE self-reloc | **T** | A13 for PIE |
| `libexec/ld.so/riscv64/ldasm.S` + `SYS.h` | 123 + stubs | `_dl_start`, `_dl_bind_start`, ld.so's own pinned syscalls | **T** | A2, A13 |
| `libexec/ld.so/riscv64/rtld_machine.c`, `archdep.h` | 306 | relocation processing | rewrite | A13 |
| `lib/libm/arch/riscv64/fenv.c`, `lib/libkvm/kvm_riscv64.c`, `usr.bin/gprof/riscv64.*` | C | | rewrite | — |

**Totals to translate:** ≈1,080 lines of kernel asm (expected to shrink to roughly half), ≈750
lines of libc asm, ≈235 of csu/ld.so asm — about **2,100 lines**, of which copy/pagezero (≈335)
collapse to block instructions and SBI/EFI/trampoline code disappears.

