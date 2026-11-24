# MD C files to write

OpenBSD base: master `c402c876540c` (2026-11-24, 8.0-current; 8.0 released 2026-10-20). Branch `pdp64`. Written 2026-11-24 from the GitHub mirror and checked against the checkout.

### MD C that must be written alongside (not assembly; listed for scope)

Core (`riscv64/riscv64/*.c`, 24 files, 10,382 lines): `pmap.c` 2187, `machdep.c` 1082, `cpu.c`
1027, `bus_dma.c` 1007, `intr.c` 769, `db_disasm.c` 608 (→ generate from the grammar codec),
`db_interface.c` 459, `conf.c` 357, `trap.c` 289, `bus_space.c` 271, `sig_machdep.c` 256, `mem.c`
254, `vm_machdep.c` 194, `clock.c` 175, `db_trace.c` 139, `process_machdep.c` 135, `disksubr.c`
131, `autoconf.c` 113, `syscall.c` 91, `ast.c` 46. **Deleted:** `fpu.c`, `vector.c`, `sbi.c`,
`openprom.c` (unless FDT is chosen). Drivers: `mainbus.c`, `pci_machdep.c`, a console driver, a
timer, an interrupt front end (≈1.5k lines); disk/net/entropy reuse MI `sys/dev/pv/{virtio,vioblk,
if_vio,viornd}.c` and `sys/dev/pci/virtio_pci.c` unchanged.

Build plumbing: `sys/arch/pdp64/conf/{GENERIC,RAMDISK,Makefile.pdp64,files.pdp64,kern.ldscript}`,
`share/mk/bsd.own.mk` (`CLANG_ARCH`, `LLD_ARCH`, `PIE_ARCH`), `Makefile.cross`,
`gnu/usr.bin/clang/Makefile.arch` + `libLLVMPDP64*` Makefiles, `etc/etc.pdp64`, `distrib/pdp64`,
`distrib/sets/lists/*/md.pdp64`.

---
