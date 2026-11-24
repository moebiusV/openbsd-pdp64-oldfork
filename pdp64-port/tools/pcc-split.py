#!/usr/bin/env python3
# Replay the fork's commits (9a993a5f..T) into three branches: dmr, pdp64, aarch64.
# Usage: pccsplit.py   (run inside the scratch clone, on a clean tree, T exists)
import subprocess, sys, re, json

BASE = '9a993a5f'
TIP = 'T'

def git(*a, check=True, input=None):
    r = subprocess.run(['git', *a], capture_output=True, text=True, input=input)
    if check and r.returncode:
        raise RuntimeError(f"git {' '.join(a)}\n{r.stdout}\n{r.stderr}")
    return r

def is_pdp64_path(f):
    return f.startswith('arch/pdp64/') or f.startswith('doc/PDP64')

def is_aarch64_path(f):
    return f.startswith('arch/aarch64/')

def owner(subject):
    if subject.startswith('pdp64') or subject.startswith('-xchecks'):
        return 'pdp64-all'
    if subject.startswith('aarch64'):
        return 'aarch64-all'
    return 'shared'

out = git('log', '--no-merges', '--reverse', '--topo-order', '--format=%H|%s', f'{BASE}..{TIP}').stdout
commits = [l.split('|', 1) for l in out.splitlines()]
for c in commits:
    c.append(owner(c[1]))
    c.append([f for f in git('diff-tree', '--no-commit-id', '--name-only', '-r', '--root', c[0]).stdout.splitlines()])

def sel(files, which):
    if which == 'dmr':
        return [f for f in files if not is_pdp64_path(f) and not is_aarch64_path(f)]
    if which == 'pdp64':
        return [f for f in files if is_pdp64_path(f)]
    return [f for f in files if is_aarch64_path(f)]

def apply_part(sha, files, log):
    """Apply the part of commit sha limited to files, staged; return True if anything staged."""
    if not files:
        return False
    d = git('diff', f'{sha}^', sha, '--binary', '--', *files).stdout
    if not d.strip():
        return False
    import os
    r = git('apply', '--3way', '--index', '--whitespace=nowarn', check=False, input=d)
    if r.returncode:
        unmerged = git('diff', '--name-only', '--diff-filter=U').stdout.split()
        err = r.stderr.strip().splitlines()
        if unmerged:
            log.append((sha[:8], 'conflict in ' + ' '.join(unmerged) + ': took the commit file'))
            targets = unmerged
        else:
            log.append((sha[:8], 'NOT APPLIED: ' + (err[-1] if err else '?') + ': took the commit files'))
            git('reset', '-q', '--hard', 'HEAD')
            targets = files
        for f in targets:
            if git('cat-file', '-e', f'{sha}:{f}', check=False).returncode == 0:
                blob = subprocess.run(['git', 'show', f'{sha}:{f}'], capture_output=True).stdout
                os.makedirs(os.path.dirname(f) or '.', exist_ok=True)
                open(f, 'wb').write(blob)
                git('add', '--', f)
            else:
                git('rm', '-q', '-f', '--ignore-unmatch', '--', f)
    return bool(git('diff', '--cached', '--name-only').stdout.strip())

def build(branch, start, wanted):
    git('checkout', '-q', '-B', branch, start)
    conflicts = []
    n = 0
    for sha, subj, own, files in commits:
        if wanted(own):
            f = files if own != 'shared' else sel(files, branch if branch != 'dmr' else 'dmr')
            if own != 'shared':
                f = files  # whole commit
        else:
            continue
        if own == 'shared':
            f = sel(files, branch)
        if apply_part(sha, f, conflicts):
            git('commit', '-q', '-C', sha, '--no-verify')
            n += 1
    return n, conflicts

res = {}
res['dmr'] = build('dmr', BASE, lambda own: own == 'shared')
dmr_tip = git('rev-parse', 'dmr').stdout.strip()
res['pdp64'] = build('pdp64', dmr_tip, lambda own: own in ('pdp64-all', 'shared'))
res['aarch64'] = build('aarch64', dmr_tip, lambda own: own in ('aarch64-all', 'shared'))
for b, (n, c) in res.items():
    print(f"{b}: {n} commits, {len(c)} conflicts resolved by taking the commit's file")
    for x in c:
        print('   ', x)
json.dump({b: [r[0], r[1]] for b, r in res.items()}, open('/tmp/pccsplit.json', 'w'))
