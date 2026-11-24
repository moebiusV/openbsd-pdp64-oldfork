#!/bin/sh
# Inventory of machine-dependent assembly (and inline-asm headers) per architecture.
# Usage: pdp64-port/tools/asm-inventory.sh [arch ...]   (default: riscv64 arm64 amd64)
# Run from anywhere; output is markdown on stdout. Read-only.
set -eu
root=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
cd "$root"
archs=${*:-riscv64 arm64 amd64}
echo "OpenBSD base: $(git rev-parse --short=12 HEAD) $(git log -1 --format=%cs)"
echo
for a in $archs; do
  echo "## $a"
  echo
  echo "| area | files | lines |"
  echo "|---|---:|---:|"
  for area in \
    "kernel:sys/arch/$a/$a" \
    "kernel-boot:sys/arch/$a/stand" \
    "libkern:sys/lib/libkern/arch/$a" \
    "libc:lib/libc/arch/$a" \
    "csu:lib/csu/$a" \
    "ld.so:libexec/ld.so/$a" \
    "libm:lib/libm/arch/$a" ; do
    name=${area%%:*}; dir=${area#*:}
    [ -d "$dir" ] || { echo "| $name | - | (no dir) |"; continue; }
    files=$(git ls-files "$dir" | grep -E '\.(S|s)$' || true)
    n=0; l=0
    for f in $files; do n=$((n+1)); l=$((l+$(wc -l <"$f"))); done
    echo "| $name | $n | $l |"
  done
  echo
  echo "### asm files"
  echo
  echo "| path | lines | symbols defined (ENTRY/END/ENTRY_NB/SYSCALL/_SYSCALL) |"
  echo "|---|---:|---|"
  for dir in sys/arch/$a/$a sys/arch/$a/stand sys/lib/libkern/arch/$a \
             lib/libc/arch/$a lib/csu/$a libexec/ld.so/$a lib/libm/arch/$a; do
    [ -d "$dir" ] || continue
    git ls-files "$dir" | grep -E '\.(S|s)$' | while read -r f; do
      syms=$(grep -hoE '^[[:space:]]*(ENTRY|ENTRY_NB|END|SYSCALL|PSEUDO|RSYSCALL|_SYSCALL|ENTRY_NP|ASENTRY)(_[A-Z]+)?\(?[[:space:]]*[A-Za-z_0-9]+' "$f" \
             | grep -vE '^[[:space:]]*(END)' | sed -E 's/^[[:space:]]*[A-Za-z_]+\(?[[:space:]]*//' | sort -u | head -12 | tr '\n' ' ')
      echo "| \`$f\` | $(wc -l <"$f") | $syms |"
    done
  done
  echo
  echo "### headers and C files containing inline asm"
  echo
  echo "| path | asm statements |"
  echo "|---|---:|"
  for dir in sys/arch/$a lib/libc/arch/$a lib/csu/$a libexec/ld.so/$a lib/libm/arch/$a; do
    [ -d "$dir" ] || continue
    git ls-files "$dir" | grep -E '\.(h|c)$' | while read -r f; do
      c=$(grep -cE '__asm|__asm__|asm[[:space:]]*(volatile)?[[:space:]]*\(' "$f" || true)
      if [ "$c" -gt 0 ]; then echo "| \`$f\` | $c |"; fi
    done
  done
  echo
done
