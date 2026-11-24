# OpenBSD on pdp64: the plan

OpenBSD base: master `c402c876540c` (2026-11-24, 8.0-current; 8.0 released 2026-10-20). Branch `pdp64`. Written 2026-11-24 from the GitHub mirror and checked against the checkout.

## Repositories (decided 2026-11-24)

| repo | what | based on |
|---|---|---|
| `pdp64` | architecture: manual, grammars, `as64`, `ld64`, `sim64`, tests | existing |
| `llvm-pdp64` | the LLVM back end (split out of `pdp64/llvm`) | `git subtree split` |
| `qemu-pdp64` | the QEMU target (split out of `pdp64/qemu`) | `git subtree split` |
| `pcc`, branches `dmr`, `pdp64`, `aarch64`, `riscv` | one repo, linked from the site as separate projects named `pcc-dmr`, `pcc-pdp64`, `pcc-aarch64` (URLs `github.com/moebiusV/pcc/tree/<branch>`) | `dmr` first, then pdp64, aarch64, riscv: it holds all the dmr/sj optimisation work and is the base the other three are rebased onto |
| `openbsd-pdp64` | this repo: OpenBSD tree on branch `pdp64`, plan in `pdp64-port/` | `openbsd/src` -current |

**Done 2026-11-24** (nothing existing was touched; all new branches):

- `moebiusV/openbsd-pdp64`: a GitHub fork of `openbsd/src`, branch `pdp64` (this plan). The
  `upstream` remote's push URL is disabled so nothing can reach `openbsd/src`.
- `moebiusV/llvm-pdp64` and `moebiusV/qemu-pdp64`: `git subtree split` of `pdp64/llvm` (31 commits)
  and `pdp64/qemu` (53 commits), history kept, plus a README note. `pdp64/llvm` and `pdp64/qemu`
  stay as they are and remain the source of truth; the scripts in the split repos still assume the
  `pdp64/<dir>` layout.
- `moebiusV/pcc` branches **`dmr-2`** (127 commits), **`pdp64-2`** (+73) and **`aarch64-2`** (+12),
  all based on upstream PortableCC `9a993a5f`; `pdp64-2` and `aarch64-2` sit on top of `dmr-2`.
  These replace an earlier push of `dmr`, `pdp64` and `aarch64` (same day), which classified
  commits by title and left optimisation work on the back-end branches; those three are still on
  the remote, superseded, until they are retired. Other branches (`master`, `single-pdp64`,
  `chk-builtins`, ...) are untouched. Built by `tools/pcc-split.py` from the union of
  `single-pdp64` and `chk-builtins` (they merge cleanly; `master` carries only cherry-picks of the
  same header-export commits).
  Rule: **everything goes to `dmr` unless it is specific to the pdp64 or the aarch64 back end**,
  judged per commit by the files and hunks it touches. So `dmr` has all of `-xchecks` (the
  front-end bounds checks, the `CHKT`/`CHKZ` operators), `-xtailcall` and `-xccp` plumbing, the
  `-xno-NAME` mechanism with `TARGET_XDEFAULTS`/`TARGET_XNO`, and the ccp type fix. Only these
  shared-file changes are back-end specific (the table `OVERRIDES` in the script): the `pdp64`
  entry in `configure`/`config.sub`, pdp64's `"; jtab"` marker in `mip/optim2.c` (-> `pdp64-2`);
  the README text on the aarch64 back end and `pr_ellidx`, which exists only for Apple varargs
  (-> `aarch64-2`).
  `cc/cc/cc.c` no longer names back ends: it asks for `TARGET_XDMR` and `TARGET_NOXSSA`, which each
  back end defines in its own `macdefs.h` (so adding a back end never edits `cc.c`, and `pdp64-2`
  and `aarch64-2` merge with no conflict; the first split had a same-line conflict there).
  Checks: `pdp64-2` merged with `aarch64-2` is conflict-free and differs from the combined tip only
  in `cc.c` and the `macdefs.h` of pdp11, powerpc, aarch64 and pdp64 (the macros); `ccom` built from
  each branch gives byte-identical assembly to the combined tip on 47 C test files for pdp64,
  pdp11, x86_64 and aarch64, including `-xchecks`; the driver passes the same `-x` options for `-O`
  on pdp11, powerpc, aarch64 and x86_64. `-xchecks` on a target without a `CHKT` lowering (x86_64)
  stops with "Cannot generate code, node op CHKT", on the combined tip as well; the comment in
  `builtins.c` says "works on every target", which is not yet true. The pdp64 driver
  (`cc/cc`) does not build for `pdp64-unknown-linux` on either, only `ccom` does.
- Not yet done: retiring the superseded `dmr`/`pdp64`/`aarch64` branches and repointing the site and `pdp64/tools/build-pcc.sh`; a `riscv` branch (nothing to split: the fork has no RISC-V work), `crunt` repo
  directory rename, pointing `pdp64/tools/build-pcc.sh` at the new branches.

Later work after the OpenBSD port itself: port the **9Frank** filesystem and the **filsys**
filesystem (the latter is a FUSE driver today).

Documents: [asm-inventory](docs/asm-inventory.md), [llvm-requirements](docs/llvm-requirements.md), [mitigation-costs](docs/mitigation-costs.md), [md-c-files](docs/md-c-files.md). Regenerate the inventory with `pdp64-port/tools/asm-inventory.sh`.

## 1. GATE: what must be ready before the cross-compiled port can boot

Three columns of prerequisites. A kernel cannot reach `init` until every **[B]** (blocker) row is
done; **[S]** rows are needed for single-user → multi-user/ssh, not for first boot.

### 1a. Architecture decisions still open in `pdp64/` (appendix J) that the port's assembly depends on

| # | Item | Why the port needs it | Where |
|---|---|---|---|
| A1 **[B]** | **Atomics**: operand placement of `CAS`/`SWAP`/`XADD`/`LL`/`SC`, and an executor that runs them (none do today) | `mutex`, `atomic.h`, `_atomic_lock`, every lock in the kernel and libc | J.7.3–J.7.5, J.9.3; impl-status |
| A2 **[B]** | **Syscall convention**: which registers carry number/args/result/error. Note `TRAP #n` only reaches n ≤ 255 and OpenBSD's syscall numbers exceed that (**verified:** `SYS_MAXSYSCALL` is 331 in `sys/sys/syscall.h`, 221 numbers defined) — so either number-in-register on one vector, or `TRAPL` widened | `SYS.h`, `syscall.c`, ld.so stubs, pinsyscalls | J.6.5 |
| A3 **[B]** | **User `DP` save/restore from kernel mode** (no sysreg number) | thread pointer at context switch, `__set_tcb`, TLS | J.6.7 |
| A4 **[B]** | **`KTBR`** number + top-level layout, and what covers the fetch after `MMUCTL` enable | pmap bootstrap, locore; the Meltdown-free split is the design's headline | J.6.4, J.6.6 |
| A5 **[B]** | **Interrupt delivery**: MSI/MSI-X → vector mapping, receiving unit (only INTx vectors 35–38 exist in QEMU) | `intr.c`, virtio-pci | J.6.3 |
| A6 **[B]** | **Timer and console form** (QEMU has a provisional compare timer and KL11-style console) | `clock.c`, console driver | J.5.1 |
| A7 **[B]** | **ABI freeze**: `R16`–`R31` roles (abi.md and appendix H disagree), stack alignment 8 vs 16, varargs form, `FPSR` save rule | every `.S` file, `cpu_switchto`, trapframe, setjmp | J.D.1, abi.md |
| A8 **[B]** | **Execute-only constant rule (P18)**: no literal pool or jump table in `.text` | OpenBSD links `--execute-only` by default | appendix H |
| A9 **[B]** | MMU discovery register (`MMUCFG`: levels, PA width); wide-PA PTE can wait | pmap | J.6.1, J.6.2 |
| A10 [S] | Landing-pad enforcement switch (page bit) + `SYS` page bit: assign PTE bits | BTI-style enforcement, pinsyscalls fast path | J.9.6, errata 84–86 |
| A11 [S] | Secondary-core start, IPI | SMP (first boot is single core) | J.4.6, J.6.3 |
| A12 [S] | Entropy source (virtio-rng), RTC | sshd keys, time | J.5.1 |
| A13 [S] | Dynamic-linking ABI: GOT form, lazy vs eager binding, TLS models, relocation numbers | ld.so, shared libc | J.D.2 |
| A14 | Security-corpus holes 6 and 7 (kernel `r2`–`r13` visible after `RTI`; `FPSR` across contexts): decide hardware fix vs kernel scrub | sets what the return-to-user path must do | `docs/security-corpus.md` |

### 1b. Emulator (`pdp64/qemu`) work

| # | Item | State today |
|---|---|---|
| Q1 **[B]** | Execute the atomic group | not in the executor |
| Q2 **[B]** | `KTBR`, ASID and `G` in the TLB model | one `PTBR`, flushes everything |
| Q3 **[B]** | RAM above 256 MiB; a boot-information block or FDT (memory ranges, console, ECAM base, bootargs) handed to `-kernel` | 128–256 MiB, nothing passed |
| Q4 **[B]** | virtio-blk (root disk) on the gpex PCIe host with a working interrupt; IOMMU either bypassable at reset or driven by the kernel | untried; IOMMU blocks DMA at reset |
| Q5 [S] | virtio-net, virtio-rng, RTC, MSI-X | absent |
| Q6 [S] | gdbstub + disassembler (debugging a kernel without them is slow) | absent |
| Q7 [S] | `-smp` | `max_cpus = 1` |

### 1c. Toolchain (detail in §3)

| # | Item | State today |
|---|---|---|
| T1 **[B]** | **Integrated assembler** (MCCodeEmitter, AsmParser, AsmBackend with length relaxation, ELF writer) driven by the grammar codec — OpenBSD's `.S` files are GNU-syntax through `clang -c`; `as64` has no `.macro`/`.section`/`.weak`/`.type`/`.size` | absent (old-encoding version frozen in `llvm/target/frozen-M1`) |
| T2 **[B]** | **clang target** `pdp64-unknown-openbsd` (TargetInfo, ABIInfo, `va_list`, driver, `__pdp64__`) | absent; clang not built |
| T3 **[B]** | **lld** `ELF/Arch/PDP64.cpp` with linker scripts, `-r`, archives, relaxation (kernel `ld.script`, KARL) | absent; `ld64` is static, two segments, no scripts |
| T4 **[B]** | Varargs, inline asm `m` constraint, `__builtin_return_address/frame_address`, atomics lowering, a real `-mgeneral-regs-only`/no-vec-block kernel switch, trap after noreturn | absent / crash |
| T5 **[B]** | Rodata in `.rodata`, relative jump tables in `.rodata`, wide/FP constants not from a `.text` pool | `.data` / `.text` pool today |
| T6 **[B]** | compiler-rt builtins for pdp64 (`__*ti3`, `__*tf3` as needed) | absent |
| T7 [S] | PIC/PIE, GOT, TLS (all four models), `.eh_frame`/CFI, debug info | absent |
| T8 [S] | OpenBSD's local LLVM passes for the target: retguard, `-fret-clean`, stack protector under PIE, landing-pad emission | absent |

**First-boot definition:** a statically linked, non-PIE kernel + ramdisk (`RAMDISK`-style `bsd.rd`)
loaded by `qemu-system-pdp64 -kernel`, single core, console only. That needs every **[B]** row and
nothing else; userland can be static first (OpenBSD supports `-static-pie`/static builds), which
defers T7/A13 past first boot but not past multi-user.

---

## 7. Later stages (after `pdp64/` settles) — outline only

R-a toolchain (§3 items 1–8) → R-b translate kernel assembly, write MD C from riscv64, static
`bsd.rd` boots to ramdisk shell in QEMU → R-c static userland, disk root, single-user → R-d PIC,
ld.so, shared libs, retguard/xonly/landing pads on → R-e virtio-net, entropy, `sshd`
(`ssh -p 2222 user@localhost`, the roadmap's finish line) → R-f SMP → **R-g port the 9Frank
filesystem and the `filsys` filesystem** to OpenBSD/pdp64 (after the port itself; `filsys` is a FUSE
driver today, so it rides on OpenBSD's `fuse(4)`/libfuse or becomes a kernel filesystem — to be
decided then).

## Assembly to translate (summary; full table in docs/asm-inventory.md and docs/translation-verdicts.md)

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

