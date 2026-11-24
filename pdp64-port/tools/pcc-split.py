#!/usr/bin/env python3
# Replay the fork's commits (9a993a5f..T) into three branches: dmr, pdp64, aarch64.
# Rule: every change goes to dmr unless it is specific to the pdp64 or the aarch64 back end.
#   - files under arch/pdp64/ and doc/PDP64*  -> pdp64;  files under arch/aarch64/ -> aarch64
#   - OVERRIDES below: shared files whose change is specific to one back end (judged per commit)
# Usage: pcc-split.py [BASE [TIP]]   (inside a clean clone where TIP exists)
import subprocess, sys, os, re, json

BASE = sys.argv[1] if len(sys.argv) > 1 else '9a993a5f'
TIP = sys.argv[2] if len(sys.argv) > 2 else 'T'

OVERRIDES = {   # (commit prefix, file) -> branch; file '*' means every shared file of the commit
    ('2fc6e13d', '*'): 'pdp64',                  # the pdp64 target in configure and config.sub
    ('fd0b3d6a', 'mip/optim2.c'): 'pdp64',       # recognises pdp64's "; jtab" marker
    ('86a001e8', 'cc/cc/cc.c'): 'skip',          # the mach_pdp64 lines: replaced by TARGET_XDMR/TARGET_NOXSSA in arch/pdp64/macdefs.h
    ('0075b3af', 'cc/cc/cc.c'): 'skip',          # the mach_aarch64 line: replaced by TARGET_XDMR in arch/aarch64/macdefs.h
    ('97da91d1', 'README.md'): 'aarch64',        # text about the aarch64 back end
    ('0041a946', '*'): 'aarch64',                # pr_ellidx: exists only for Apple's varargs
}
FIXERS = {}

def git(*a, check=True, input=None):
    r = subprocess.run(['git', *a], capture_output=True, text=True, input=input)
    if check and r.returncode:
        raise RuntimeError(f"git {' '.join(a)}\n{r.stdout}\n{r.stderr}")
    return r

def route(sha, f):
    if f.startswith('arch/pdp64/') or f.startswith('doc/PDP64'): return 'pdp64'
    if f.startswith('arch/aarch64/'): return 'aarch64'
    for (p, g), b in OVERRIDES.items():
        if sha.startswith(p) and g in ('*', f): return b
    return 'dmr'

out = git('log', '--no-merges', '--reverse', '--topo-order', '--format=%H|%s', f'{BASE}..{TIP}').stdout
commits = []
for l in out.splitlines():
    h, s = l.split('|', 1)
    files = git('diff-tree', '--no-commit-id', '--name-only', '-r', '--root', h).stdout.splitlines()
    commits.append((h, s, files))

def apply_part(sha, files, branch, log):
    if not files: return False
    d = git('diff', f'{sha}^', sha, '--binary', '--', *files).stdout
    if not d.strip(): return False
    r = git('apply', '--3way', '--index', '--whitespace=nowarn', check=False, input=d)
    if r.returncode:
        unmerged = git('diff', '--name-only', '--diff-filter=U').stdout.split()
        if unmerged:
            targets = unmerged
        else:
            git('reset', '-q', '--hard', 'HEAD'); targets = files
        for f in targets:
            fx = FIXERS.get((sha[:8], branch, f))
            if fx:
                head = git('show', f'HEAD:{f}').stdout
                new = fx(head)
                assert new != head, f'fixer did nothing for {sha[:8]} {f}'
                open(f, 'w').write(new); git('add', '--', f)
                log.append((sha[:8], f'{f}: resolved by a targeted edit'))
            elif git('cat-file', '-e', f'{sha}:{f}', check=False).returncode == 0:
                blob = subprocess.run(['git', 'show', f'{sha}:{f}'], capture_output=True).stdout
                os.makedirs(os.path.dirname(f) or '.', exist_ok=True)
                open(f, 'wb').write(blob); git('add', '--', f)
                log.append((sha[:8], f'{f}: took the commit file ({"conflict" if unmerged else "NOT APPLIED"})'))
            else:
                git('rm', '-q', '-f', '--ignore-unmatch', '--', f)
    return bool(git('diff', '--cached', '--name-only').stdout.strip())

def build(branch, start):
    git('checkout', '-q', '-B', branch, start)
    log = []; n = 0
    for sha, subj, files in commits:
        mine = [f for f in files if route(sha, f) == branch]
        if apply_part(sha, mine, branch, log):
            git('commit', '-q', '-C', sha, '--no-verify'); n += 1
    return n, log


def commit_all(msg):
    git('add', '-A')
    if git('diff', '--cached', '--name-only').stdout.strip():
        git('commit', '-q', '--no-verify', '-m', msg)

def append(path, text):
    old = open(path).read() if os.path.exists(path) else ''
    open(path, 'w').write(old.rstrip('\n') + '\n' + text)

def restructure_dmr():
    git('checkout', '-q', 'dmr')
    t = open('cc/cc/cc.c').read()
    old_dmr = '#ifdef mach_pdp11\n\t{ &Oflag, 1, "-xdmr" },\t/* -O here has always meant dmr-cc\'s code */\n#endif\n'
    new_dmr = '#ifdef TARGET_XDMR\t/* -O means dmr-cc\'s code on this target (-xdmr); the target sets it in macdefs.h */\n\t{ &Oflag, 1, "-xdmr" },\n#endif\n'
    assert old_dmr in t
    t = t.replace(old_dmr, new_dmr, 1)
    t, n = re.subn(r'#if !defined\(PCC_NO_SSA\) && !defined\(mach_aarch64\) && !defined\(mach_powerpc\)[^\n]*',
        '#if !defined(PCC_NO_SSA) && !defined(TARGET_NOXSSA)\t/* a target sets TARGET_NOXSSA in macdefs.h when -xssa hurts it */', t, count=1)
    assert n == 1
    open('cc/cc/cc.c', 'w').write(t)
    append('arch/pdp11/macdefs.h', '\n/* -O means dmr-cc\'s code on this target: the driver (cc.c) passes -xdmr */\n#define\tTARGET_XDMR\n')
    append('arch/powerpc/macdefs.h', '\n/* -xssa makes powerpc code 2% bigger: the driver (cc.c) leaves it out of -O */\n#define\tTARGET_NOXSSA\n')
    append('arch/aarch64/macdefs.h', '\n/* -xssa breaks varargs and structs here: the driver (cc.c) leaves it out of -O */\n#define\tTARGET_NOXSSA\n')
    commit_all("cc: the target says in macdefs.h whether -O means -xdmr and whether it leaves out -xssa\n\n"
      "The driver tested mach_pdp11, mach_aarch64 and mach_powerpc by name, so every back end that\n"
      "wanted the same defaults edited the same two lines of cc.c.  Now cc.c asks for TARGET_XDMR and\n"
      "TARGET_NOXSSA, which a back end defines in its own macdefs.h (as TARGET_XDEFAULTS and\n"
      "TARGET_XNO already work in ccom).  No change in behaviour for pdp11, powerpc or aarch64.")

def after_replay(branch):
    git('checkout', '-q', branch)
    if branch == 'pdp64':
        append('arch/pdp64/macdefs.h', '\n/* -O means dmr-cc\'s code here (-xdmr) and leaves out -xssa, which makes pdp64 code 1% bigger: see cc.c */\n#define\tTARGET_XDMR\n#define\tTARGET_NOXSSA\n')
        commit_all("pdp64: -O means -xdmr and leaves out -xssa (TARGET_XDMR, TARGET_NOXSSA in macdefs.h)")
    else:
        t = open('arch/aarch64/macdefs.h').read()
        add = ''
        if 'TARGET_NOXSSA' not in t:
            add += '\n/* -xssa breaks varargs and structs here: the driver (cc.c) leaves it out of -O */\n#define\tTARGET_NOXSSA\n'
        add += '\n/* -O means dmr-cc\'s code here (-xdmr; peep.h): see cc.c */\n#define\tTARGET_XDMR\n'
        append('arch/aarch64/macdefs.h', add)
        commit_all("aarch64: -O means -xdmr (TARGET_XDMR in macdefs.h)")

res = {'dmr': build('dmr', BASE)}
restructure_dmr()
dmr_tip = git('rev-parse', 'dmr').stdout.strip()
res['pdp64'] = build('pdp64', dmr_tip)
res['aarch64'] = build('aarch64', dmr_tip)
for b in ('pdp64', 'aarch64'): after_replay(b)
for b, (n, c) in res.items():
    print(f"{b}: {n} commits")
    for x in c: print('   ', x)
