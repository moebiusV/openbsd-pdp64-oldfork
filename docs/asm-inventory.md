OpenBSD base: c402c876540c 2026-11-24

## riscv64

| area | files | lines |
|---|---:|---:|
| kernel | 8 | 1082 |
| kernel-boot | 1 | 170 |
| libkern | - | (no dir) |
| libc | 11 | 751 |
| csu | 0 | 0 |
| ld.so | 1 | 123 |
| libm | 0 | 0 |

### asm files

| path | lines | symbols defined (ENTRY/END/ENTRY_NB/SYSCALL/_SYSCALL) |
|---|---:|---|
| `sys/arch/riscv64/riscv64/copy.S` | 177 | copyin copyin32 copyout kcopy  |
| `sys/arch/riscv64/riscv64/copystr.S` | 116 | copyinstr copyoutstr  |
| `sys/arch/riscv64/riscv64/cpuswitch.S` | 99 | cpu_switchto_asm proc_trampoline  |
| `sys/arch/riscv64/riscv64/exception.S` | 244 | cpu_exception_handler cpu_exception_handler_supervisor cpu_exception_handler_user syscall_return  |
| `sys/arch/riscv64/riscv64/locore.S` | 268 | sigcode  |
| `sys/arch/riscv64/riscv64/locore0.S` | 47 |  |
| `sys/arch/riscv64/riscv64/pagezero.S` | 42 | pagezero  |
| `sys/arch/riscv64/riscv64/support.S` | 89 | longjmp setjmp  |
| `sys/arch/riscv64/stand/efiboot/start.S` | 170 |  |
| `lib/libc/arch/riscv64/gen/_setjmp.S` | 114 | _longjmp _setjmp  |
| `lib/libc/arch/riscv64/gen/setjmp.S` | 129 | longjmp setjmp  |
| `lib/libc/arch/riscv64/gen/sigsetjmp.S` | 133 | siglongjmp sigsetjmp  |
| `lib/libc/arch/riscv64/sys/Ovfork.S` | 41 |   |
| `lib/libc/arch/riscv64/sys/brk.S` | 59 | brk  |
| `lib/libc/arch/riscv64/sys/sbrk.S` | 50 | sbrk  |
| `lib/libc/arch/riscv64/sys/sigpending.S` | 43 | sigpending  |
| `lib/libc/arch/riscv64/sys/sigprocmask.S` | 52 |   |
| `lib/libc/arch/riscv64/sys/sigsuspend.S` | 42 |   |
| `lib/libc/arch/riscv64/sys/syscall.S` | 35 | syscall  |
| `lib/libc/arch/riscv64/sys/tfork_thread.S` | 53 | __tfork_thread  |
| `libexec/ld.so/riscv64/ldasm.S` | 123 | _dl_bind_start _rtld_tlsdesc  |

### headers and C files containing inline asm

| path | asm statements |
|---|---:|
| `sys/arch/riscv64/dev/sfcc.c` | 2 |
| `sys/arch/riscv64/include/atomic.h` | 3 |
| `sys/arch/riscv64/include/bus.h` | 9 |
| `sys/arch/riscv64/include/cdefs.h` | 3 |
| `sys/arch/riscv64/include/cpu.h` | 5 |
| `sys/arch/riscv64/include/cpufunc.h` | 7 |
| `sys/arch/riscv64/include/profile.h` | 3 |
| `sys/arch/riscv64/include/riscvreg.h` | 9 |
| `sys/arch/riscv64/include/sbi.h` | 7 |
| `sys/arch/riscv64/include/tcb.h` | 1 |
| `sys/arch/riscv64/riscv64/bus_dma.c` | 1 |
| `sys/arch/riscv64/riscv64/bus_space.c` | 21 |
| `sys/arch/riscv64/riscv64/cpu.c` | 12 |
| `sys/arch/riscv64/riscv64/db_disasm.c` | 1 |
| `sys/arch/riscv64/riscv64/db_interface.c` | 1 |
| `sys/arch/riscv64/riscv64/fpu.c` | 7 |
| `sys/arch/riscv64/riscv64/machdep.c` | 4 |
| `sys/arch/riscv64/riscv64/pmap.c` | 2 |
| `sys/arch/riscv64/riscv64/vector.c` | 11 |
| `sys/arch/riscv64/stand/efiboot/exec.c` | 2 |
| `lib/libc/arch/riscv64/gen/_atomic_lock.c` | 1 |
| `lib/libc/arch/riscv64/gen/flt_rounds.c` | 1 |
| `lib/libc/arch/riscv64/gen/fpgetround.c` | 1 |
| `lib/libc/arch/riscv64/gen/fpgetsticky.c` | 1 |
| `lib/libc/arch/riscv64/gen/fpsetround.c` | 1 |
| `lib/libc/arch/riscv64/gen/fpsetsticky.c` | 1 |
| `lib/libc/arch/riscv64/gen/usertc.c` | 1 |
| `lib/csu/riscv64/md_init.h` | 5 |
| `libexec/ld.so/riscv64/rtld_machine.c` | 5 |
| `lib/libm/arch/riscv64/fenv.c` | 6 |

## arm64

| area | files | lines |
|---|---:|---:|
| kernel | 12 | 3790 |
| kernel-boot | 2 | 1149 |
| libkern | 1 | 17 |
| libc | - | (no dir) |
| csu | - | (no dir) |
| ld.so | - | (no dir) |
| libm | - | (no dir) |

### asm files

| path | lines | symbols defined (ENTRY/END/ENTRY_NB/SYSCALL/_SYSCALL) |
|---|---:|---|
| `sys/arch/arm64/arm64/aesv8-armx.S` | 1154 |  |
| `sys/arch/arm64/arm64/copy.S` | 221 | copyin copyin32 copyout kcopy  |
| `sys/arch/arm64/arm64/copystr.S` | 105 | copyinstr copyoutstr  |
| `sys/arch/arm64/arm64/cpufunc_asm.S` | 253 | aplcpu_deep_wfi cpu_dcache_inv_range cpu_dcache_wbinv_range cpu_dcache_wb_range cpu_icache_sync_range cpu_idcache_wbinv_range cpu_setttb cpu_tlb_flush cpu_tlb_flush_all_asid cpu_tlb_flush_asid cpu_tlb_flush_asid_all cpu_wfi  |
| `sys/arch/arm64/arm64/cpuswitch.S` | 88 | cpu_switchto_asm proc_trampoline  |
| `sys/arch/arm64/arm64/exception.S` | 291 | syscall_return  |
| `sys/arch/arm64/arm64/hibernate_asm.S` | 193 | hibernate_activate_resume_pt_machdep hibernate_dcache_flush_machdep hibernate_flush hibernate_resume_machdep hibernate_retguard_copy_machdep hibernate_switch_stack_machdep  |
| `sys/arch/arm64/arm64/locore.S` | 561 |  |
| `sys/arch/arm64/arm64/locore0.S` | 400 |  |
| `sys/arch/arm64/arm64/lse.S` | 170 | __aarch64_cas4_acq_rel __aarch64_cas8_acq_rel __aarch64_ldadd4_acq_rel __aarch64_ldadd8_acq_rel __aarch64_ldclr4_acq_rel __aarch64_ldset4_acq_rel __aarch64_swp4_acq_rel __aarch64_swp8_acq_rel  |
| `sys/arch/arm64/arm64/support.S` | 134 | hvc_call longjmp pagezero_cache pagezero_simple setjmp smc_call  |
| `sys/arch/arm64/arm64/trampoline.S` | 220 |  |
| `sys/arch/arm64/stand/efiboot/dt_blob.S` | 973 |  |
| `sys/arch/arm64/stand/efiboot/start.S` | 176 |  |
| `sys/lib/libkern/arch/arm64/ffs.S` | 17 | ffs  |

### headers and C files containing inline asm

| path | asm statements |
|---|---:|
| `sys/arch/arm64/arm64/cpu.c` | 23 |
| `sys/arch/arm64/arm64/db_disasm.c` | 2 |
| `sys/arch/arm64/arm64/db_interface.c` | 1 |
| `sys/arch/arm64/arm64/disasm.c` | 1 |
| `sys/arch/arm64/arm64/disasm.h` | 1 |
| `sys/arch/arm64/arm64/fpu.c` | 11 |
| `sys/arch/arm64/arm64/hibernate_machdep.c` | 2 |
| `sys/arch/arm64/arm64/machdep.c` | 3 |
| `sys/arch/arm64/arm64/pmap.c` | 16 |
| `sys/arch/arm64/dev/agintc.c` | 25 |
| `sys/arch/arm64/dev/agtimer.c` | 13 |
| `sys/arch/arm64/dev/apldart.c` | 2 |
| `sys/arch/arm64/dev/bcm2836_intr.c` | 1 |
| `sys/arch/arm64/dev/efi_machdep.c` | 2 |
| `sys/arch/arm64/include/armreg.h` | 2 |
| `sys/arch/arm64/include/atomic.h` | 3 |
| `sys/arch/arm64/include/bus.h` | 1 |
| `sys/arch/arm64/include/cdefs.h` | 3 |
| `sys/arch/arm64/include/cpu.h` | 8 |
| `sys/arch/arm64/include/profile.h` | 3 |
| `sys/arch/arm64/include/tcb.h` | 2 |
| `sys/arch/arm64/stand/efiboot/efiboot.c` | 4 |
| `sys/arch/arm64/stand/efiboot/exec.c` | 3 |

## amd64

| area | files | lines |
|---|---:|---:|
| kernel | 11 | 7571 |
| kernel-boot | 12 | 3629 |
| libkern | 17 | 906 |
| libc | 34 | 3259 |
| csu | 0 | 0 |
| ld.so | 1 | 145 |
| libm | 41 | 1095 |

### asm files

| path | lines | symbols defined (ENTRY/END/ENTRY_NB/SYSCALL/_SYSCALL) |
|---|---:|---|
| `sys/arch/amd64/amd64/acpi_wakecode.S` | 827 |  |
| `sys/arch/amd64/amd64/aes_intel.S` | 1187 | aesni_cbc_dec aesni_cbc_enc aesni_ctr_enc aesni_dec aesni_ecb_dec aesni_ecb_enc aesni_enc aesni_gmac_final aesni_gmac_update aesni_set_key aesni_xts_dec aesni_xts_enc  |
| `sys/arch/amd64/amd64/copy.S` | 307 | _copyin _copyinstr copyout copyoutstr copystr_fault kcopy  |
| `sys/arch/amd64/amd64/kexec_subr.S` | 138 |  |
| `sys/arch/amd64/amd64/locore.S` | 1237 |  cpu_idle_cycle_hlt cpu_switchto fpusave fpusavereset longjmp pagezero pku_xonly rdmsr_safe savectx setjmp xrstor_kern  |
| `sys/arch/amd64/amd64/locore0.S` | 930 |  |
| `sys/arch/amd64/amd64/mds.S` | 199 | mds_handler_bdw mds_handler_ivb mds_handler_knights mds_handler_silvermont mds_handler_skl mds_handler_skl_avx mds_handler_skl_avx512 mds_handler_skl_sse  |
| `sys/arch/amd64/amd64/mptramp.S` | 272 |  |
| `sys/arch/amd64/amd64/spl.S` | 172 |  |
| `sys/arch/amd64/amd64/vector.S` | 1477 |  |
| `sys/arch/amd64/amd64/vmm_support.S` | 825 | invept invvpid svm_enter_guest svm_seves_enter_guest vmclear vmptrld vmptrst vmread vmwrite vmx_enter_guest vmxoff vmxon  |
| `sys/arch/amd64/stand/biosboot/biosboot.S` | 862 |  |
| `sys/arch/amd64/stand/boot/srt0.S` | 92 |  |
| `sys/arch/amd64/stand/cdboot/srt0.S` | 267 | debugchar  |
| `sys/arch/amd64/stand/cdbr/cdbr.S` | 529 |  |
| `sys/arch/amd64/stand/efiboot/run_i386.S` | 115 |  |
| `sys/arch/amd64/stand/efiboot/start_amd64.S` | 76 |  |
| `sys/arch/amd64/stand/efiboot/start_i386.S` | 68 | _start  |
| `sys/arch/amd64/stand/libsa/gidt.S` | 465 | bootbuf _rtt  |
| `sys/arch/amd64/stand/libsa/pxe_call.S` | 212 | pxecall_bangpxe pxecall_pxenv  |
| `sys/arch/amd64/stand/libsa/run_amd64.S` | 175 |  |
| `sys/arch/amd64/stand/mbr/mbr.S` | 521 |  |
| `sys/arch/amd64/stand/pxeboot/srt0.S` | 247 | debugchar  |
| `sys/lib/libkern/arch/amd64/bcmp.S` | 23 | bcmp  |
| `sys/lib/libkern/arch/amd64/bcopy.S` | 1 |  |
| `sys/lib/libkern/arch/amd64/bzero.S` | 42 | bzero  |
| `sys/lib/libkern/arch/amd64/ffs.S` | 21 | ffs  |
| `sys/lib/libkern/arch/amd64/index.S` | 1 |  |
| `sys/lib/libkern/arch/amd64/memchr.S` | 24 | memchr  |
| `sys/lib/libkern/arch/amd64/memcmp.S` | 39 | memcmp  |
| `sys/lib/libkern/arch/amd64/memcpy.S` | 1 |  |
| `sys/lib/libkern/arch/amd64/memmove.S` | 94 | bcopy memcpy  |
| `sys/lib/libkern/arch/amd64/memset.S` | 56 | memset  |
| `sys/lib/libkern/arch/amd64/rindex.S` | 1 |  |
| `sys/lib/libkern/arch/amd64/scanc.S` | 58 | scanc  |
| `sys/lib/libkern/arch/amd64/skpc.S` | 52 | skpc  |
| `sys/lib/libkern/arch/amd64/strchr.S` | 131 | strchr  |
| `sys/lib/libkern/arch/amd64/strcmp.S` | 75 | strcmp  |
| `sys/lib/libkern/arch/amd64/strlen.S` | 160 | strlen  |
| `sys/lib/libkern/arch/amd64/strrchr.S` | 127 | strrchr  |
| `lib/libc/arch/amd64/gen/_setjmp.S` | 109 | _longjmp _setjmp  |
| `lib/libc/arch/amd64/gen/fabs.S` | 20 | fabs  |
| `lib/libc/arch/amd64/gen/flt_rounds.S` | 32 | __flt_rounds  |
| `lib/libc/arch/amd64/gen/fpgetmask.S` | 34 | _fpgetmask fpgetmask  |
| `lib/libc/arch/amd64/gen/fpgetround.S` | 33 | _fpgetround fpgetround  |
| `lib/libc/arch/amd64/gen/fpgetsticky.S` | 35 | _fpgetsticky fpgetsticky  |
| `lib/libc/arch/amd64/gen/fpsetmask.S` | 49 | _fpsetmask fpsetmask  |
| `lib/libc/arch/amd64/gen/fpsetround.S` | 56 | _fpsetround fpsetround  |
| `lib/libc/arch/amd64/gen/fpsetsticky.S` | 53 | _fpsetsticky fpsetsticky  |
| `lib/libc/arch/amd64/gen/setjmp.S` | 133 | longjmp setjmp  |
| `lib/libc/arch/amd64/gen/sigsetjmp.S` | 133 | siglongjmp sigsetjmp  |
| `lib/libc/arch/amd64/hash/sha1_amd64_generic.S` | 310 | __sha1_block_generic  |
| `lib/libc/arch/amd64/hash/sha1_amd64_shani.S` | 163 | __sha1_block_shani  |
| `lib/libc/arch/amd64/hash/sha256_amd64_generic.S` | 299 | __sha256_block_generic  |
| `lib/libc/arch/amd64/hash/sha256_amd64_shani.S` | 203 | __sha256_block_shani  |
| `lib/libc/arch/amd64/hash/sha512_amd64_generic.S` | 304 | __sha512_block_generic  |
| `lib/libc/arch/amd64/string/bcmp.S` | 23 | bcmp  |
| `lib/libc/arch/amd64/string/bzero.S` | 43 | bzero  |
| `lib/libc/arch/amd64/string/ffs.S` | 22 | ffs  |
| `lib/libc/arch/amd64/string/memchr.S` | 24 | memchr  |
| `lib/libc/arch/amd64/string/memmove.S` | 98 | bcopy memcpy  |
| `lib/libc/arch/amd64/string/memset.S` | 58 | memset  |
| `lib/libc/arch/amd64/string/strchr.S` | 130 | strchr  |
| `lib/libc/arch/amd64/string/strcmp.S` | 74 | strcmp  |
| `lib/libc/arch/amd64/string/strlen.S` | 159 | strlen  |
| `lib/libc/arch/amd64/string/strrchr.S` | 126 | strrchr  |
| `lib/libc/arch/amd64/sys/Ovfork.S` | 62 |   |
| `lib/libc/arch/amd64/sys/brk.S` | 70 | brk  |
| `lib/libc/arch/amd64/sys/sbrk.S` | 75 | sbrk  |
| `lib/libc/arch/amd64/sys/sigpending.S` | 50 | sigpending  |
| `lib/libc/arch/amd64/sys/sigprocmask.S` | 64 |   |
| `lib/libc/arch/amd64/sys/sigsuspend.S` | 51 |   |
| `lib/libc/arch/amd64/sys/syscall.S` | 56 | syscall  |
| `lib/libc/arch/amd64/sys/tfork_thread.S` | 108 | __tfork_thread  |
| `libexec/ld.so/amd64/ldasm.S` | 145 |  |
| `lib/libm/arch/amd64/e_acos.S` | 26 | acos  |
| `lib/libm/arch/amd64/e_asin.S` | 25 | asin  |
| `lib/libm/arch/amd64/e_atan2.S` | 20 | atan2  |
| `lib/libm/arch/amd64/e_atan2f.S` | 20 | atan2f  |
| `lib/libm/arch/amd64/e_exp.S` | 106 | exp  |
| `lib/libm/arch/amd64/e_fmod.S` | 25 | fmod  |
| `lib/libm/arch/amd64/e_log.S` | 20 | log  |
| `lib/libm/arch/amd64/e_log10.S` | 20 | log10  |
| `lib/libm/arch/amd64/e_remainder.S` | 24 | remainder  |
| `lib/libm/arch/amd64/e_remainderf.S` | 24 | remainderf  |
| `lib/libm/arch/amd64/e_scalb.S` | 21 | scalb  |
| `lib/libm/arch/amd64/e_sqrt.S` | 15 | sqrt  |
| `lib/libm/arch/amd64/e_sqrtf.S` | 15 | sqrtf  |
| `lib/libm/arch/amd64/e_sqrtl.S` | 16 | sqrtl  |
| `lib/libm/arch/amd64/s_atan.S` | 20 | atan  |
| `lib/libm/arch/amd64/s_atanf.S` | 20 | atanf  |
| `lib/libm/arch/amd64/s_ceil.S` | 27 | ceil  |
| `lib/libm/arch/amd64/s_ceilf.S` | 25 | ceilf  |
| `lib/libm/arch/amd64/s_copysign.S` | 26 | copysign  |
| `lib/libm/arch/amd64/s_copysignf.S` | 26 | copysignf  |
| `lib/libm/arch/amd64/s_cos.S` | 34 | cos  |
| `lib/libm/arch/amd64/s_cosf.S` | 20 | cosf  |
| `lib/libm/arch/amd64/s_floor.S` | 26 | floor  |
| `lib/libm/arch/amd64/s_floorf.S` | 26 | floorf  |
| `lib/libm/arch/amd64/s_llrint.S` | 14 | llrint  |
| `lib/libm/arch/amd64/s_llrintf.S` | 15 | llrintf  |
| `lib/libm/arch/amd64/s_log1p.S` | 77 | log1p  |
| `lib/libm/arch/amd64/s_log1pf.S` | 77 | log1pf  |
| `lib/libm/arch/amd64/s_logb.S` | 20 | logb  |
| `lib/libm/arch/amd64/s_logbf.S` | 20 | logbf  |
| `lib/libm/arch/amd64/s_lrint.S` | 14 | lrint  |
| `lib/libm/arch/amd64/s_lrintf.S` | 14 | lrintf  |
| `lib/libm/arch/amd64/s_rint.S` | 19 | rint  |
| `lib/libm/arch/amd64/s_rintf.S` | 19 | rintf  |
| `lib/libm/arch/amd64/s_scalbnf.S` | 26 | scalbnf  |
| `lib/libm/arch/amd64/s_significand.S` | 21 | significand  |
| `lib/libm/arch/amd64/s_significandf.S` | 21 | significandf  |
| `lib/libm/arch/amd64/s_sin.S` | 34 | sin  |
| `lib/libm/arch/amd64/s_sinf.S` | 20 | sinf  |
| `lib/libm/arch/amd64/s_tan.S` | 36 | tan  |
| `lib/libm/arch/amd64/s_tanf.S` | 21 | tanf  |

### headers and C files containing inline asm

| path | asm statements |
|---|---:|
| `sys/arch/amd64/amd64/bus_space.c` | 22 |
| `sys/arch/amd64/amd64/cpu.c` | 2 |
| `sys/arch/amd64/amd64/db_disasm.c` | 1 |
| `sys/arch/amd64/amd64/db_interface.c` | 8 |
| `sys/arch/amd64/amd64/efi_machdep.c` | 1 |
| `sys/arch/amd64/amd64/intr.c` | 1 |
| `sys/arch/amd64/amd64/ipifuncs.c` | 1 |
| `sys/arch/amd64/amd64/kexec.c` | 1 |
| `sys/arch/amd64/amd64/lapic.c` | 3 |
| `sys/arch/amd64/amd64/machdep.c` | 2 |
| `sys/arch/amd64/amd64/pctr.c` | 4 |
| `sys/arch/amd64/amd64/via.c` | 3 |
| `sys/arch/amd64/include/atomic.h` | 24 |
| `sys/arch/amd64/include/bus.h` | 3 |
| `sys/arch/amd64/include/cdefs.h` | 3 |
| `sys/arch/amd64/include/cpu.h` | 4 |
| `sys/arch/amd64/include/cpufunc.h` | 46 |
| `sys/arch/amd64/include/fpu.h` | 7 |
| `sys/arch/amd64/include/intr.h` | 1 |
| `sys/arch/amd64/include/pctr.h` | 1 |
| `sys/arch/amd64/include/pio.h` | 18 |
| `sys/arch/amd64/include/profile.h` | 1 |
| `sys/arch/amd64/include/specialreg.h` | 2 |
| `sys/arch/amd64/include/tcb.h` | 1 |
| `sys/arch/amd64/stand/efiboot/efiboot.c` | 2 |
| `sys/arch/amd64/stand/efiboot/exec_i386.c` | 4 |
| `sys/arch/amd64/stand/libsa/bioscons.c` | 6 |
| `sys/arch/amd64/stand/libsa/biosdev.c` | 5 |
| `sys/arch/amd64/stand/libsa/biosprobe.c` | 2 |
| `sys/arch/amd64/stand/libsa/mdrandom.c` | 3 |
| `sys/arch/amd64/stand/libsa/memprobe.c` | 3 |
| `sys/arch/amd64/stand/libsa/time.c` | 1 |
| `lib/libc/arch/amd64/gen/_atomic_lock.c` | 1 |
| `lib/libc/arch/amd64/gen/ldexp.c` | 1 |
| `lib/libc/arch/amd64/gen/usertc.c` | 2 |
| `lib/csu/amd64/md_init.h` | 5 |
| `libexec/ld.so/amd64/rtld_machine.c` | 5 |
| `lib/libm/arch/amd64/fenv.c` | 38 |

