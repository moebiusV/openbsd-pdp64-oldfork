# OpenBSD on the pdp64

The plan for porting OpenBSD to the [pdp64](https://moebiusv.github.io/pdp64/), a 64-bit successor to the PDP-11. The first thing it says is what has to be ready before a cross-compiled OpenBSD can boot in QEMU; the port itself is written once the pdp64 settles.

- [The plan](PLAN.md): what must be ready first (architecture decisions, the emulator, the toolchain), the repositories, and what is done.
- [Assembly inventory](docs/asm-inventory.md) and [translation verdicts](docs/translation-verdicts.md): every assembly file the port needs, taken from the riscv64 and arm64 ports, and what happens to each on the pdp64.
- [What LLVM, clang and lld must provide](docs/llvm-requirements.md).
- [What each OpenBSD policy and mitigation costs on the pdp64](docs/mitigation-costs.md): where the design makes it cheaper, and where it does not.
- [The machine-dependent C files to write](docs/md-c-files.md).

Source of these pages: the `pdp64` branch of this repository, directory `pdp64-port/`. This branch holds only a copy, for Pages.
