# What LLVM, clang and lld must provide

OpenBSD base: master `c402c876540c` (2026-11-24, 8.0-current; 8.0 released 2026-10-20). Branch `pdp64`. Written 2026-11-24 from the GitHub mirror and checked against the checkout.


Ordered by when the port needs it. Base: `pdp64/llvm/target/PDP64` on LLVM 21.1.8.

**Before any kernel object compiles**
1. MC layer on the *current* encoding, calling the grammar-generated table codec
   (`common/pdp64enc.c`) so renumbering opcodes never touches LLVM: CodeEmitter, AsmParser (GNU
   directives come free from the generic ELF parser), Disassembler, AsmBackend with
   `relaxInstruction` for 2/4/6-byte forms, ELFObjectWriter. Reconcile `ELFRelocs/PDP64.def` with
   `as64/relocs.h` (missing `ALIGN`, `D32_PC`) and make one of them generated.
2. clang: `Triple` OS=openbsd behaviour, `clang/lib/Basic/Targets/PDP64.{h,cpp}`,
   `CodeGen/Targets/PDP64.cpp` (struct passing ≤16 bytes in `R0:R1`, hidden pointer in `R0`,
   `va_list = char *`), `Driver/ToolChains/OpenBSD.cpp` arch cases, predefined macros.
3. Codegen holes found by running `llc`: varargs (3 `report_fatal_error` sites in
   `PDP64ISelLowering.cpp`), `m` inline-asm operands, return/frame address, `fence`, trap after
   noreturn calls, frame pointer honoured for `-fno-omit-frame-pointer` (ddb stack traces).
4. Atomics: lower `atomicrmw`/`cmpxchg`/atomic load-store to `CAS`/`SWAP`/`XADD`/… (after A1);
   memory model is sequentially consistent so every `membar_*` is empty.
5. Kernel mode switch: a target feature that turns off `-pdp64-vecblock` lowering (kernel must not
   use `vec` blocks in interrupt paths); FP is in GPRs so there is no FP-register ban to implement —
   but decide whether kernel code may touch `FPSR`.
6. Section hygiene for execute-only: `.rodata` for constants, PC-relative 32-bit jump-table entries
   in `.rodata`, wide constants materialised or loaded from `.rodata` (rule A8).
7. lld port: relocation application through the codec (the `INSN_*` relocs don't encode the field
   position), relaxation pass (model on lld's RISC-V relaxation), linker scripts/`-r`/archives come
   from lld generic code; `PT_OPENBSD_*` segments already exist in OpenBSD's lld.
8. compiler-rt builtins, then libunwind/libc++ later.

**Before dynamic userland**
9. PIC/PIE (`d(PC)` data, `got(PC)` imports), GOT/PLT decision, dynamic relocs
   (`RELATIVE`, `GLOB_DAT`, `JUMP_SLOT`, `COPY`, `TPOFF`/`DTPMOD`/`DTPOFF`), TLS models via user `DP`.
10. `.eh_frame`/CFI (DWARF numbers 0–31 already generated), debug info.

**OpenBSD-specific passes** (ported from OpenBSD's `gnu/llvm`, not upstream)
11. Retguard (`ReturnProtectorLowering` for PDP64): the return address is on the stack at a known
    slot, so the amd64 shape applies — load cookie from `.openbsd.randomdata`, XOR with the saved
    return address on entry, re-XOR and `ct ne` (a check instruction → vector 16, no separate trap
    sled) before `RET`.
12. `-fret-clean` (zero the return-address slot after return), stack protector under PIE,
    `LPAD` at address-taken function entries and `JTAG` targets, syscall stubs emitted so
    `pinsyscalls` can record each `TRAP` site.

**Which LLVM:** OpenBSD's import commits (2026-05-29) say **LLVM 21.1.6** — the same 21.1.x line as
the pdp64 back end (21.1.8). *Open check:* `gnu/usr.bin/clang/include/llvm/Config/llvm-config.h.in`
says `22.1.6` although it was updated by the "build infrastructure for llvm-21.1.6" commit; find out
which is right before copying the target in. So the target directory drops into `gnu/llvm/llvm/lib/Target/PDP64`
nearly unchanged, and OpenBSD's own passes (retguard at
`llvm/lib/CodeGen/ReturnProtectorLowering.cpp`, lld's `--execute-only`, `-z nobtcfi`,
`PT_OPENBSD_SYSCALLS`) are already there. Plan: keep developing in `~/claude/llvm-project`, and
build the cross compiler **from OpenBSD's `gnu/llvm` tree on Linux** with the PDP64 target copied
in, so the cross toolchain has the OpenBSD passes. Note retguard today exists only for amd64,
arm64, powerpc, mips64 — **riscv64 has none** (`#error RETGUARD not yet supported`), so a
`PDP64ReturnProtectorLowering` modelled on the X86 one is new work, and pdp64 would be the first
non-x86 target with `-fret-clean`.

---
