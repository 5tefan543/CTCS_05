#!/usr/bin/env python3

import sys
import json

DEFAULT_FILENAME = 'enerjstats.json'

def showstatblock(items, unit='ops'):
    for name, (precise, approx) in items:
        total = precise + approx
        frac = float(approx) / total
        print(f'  {name}: {total} {unit} total, {frac * 100:.1f}% approx')

def showstats(stats):
    ops_arith = []
    ops_mem = []
    for name, vals in stats['operations'].items():
        if name.startswith('load') or name.startswith('store'):
            ops_mem.append((name, vals))
        else:
            ops_arith.append((name, vals))
    ops_mem.sort()
    ops_arith.sort()
    
    footprint = []
    for name, vals in stats['footprint'].items():
        section, kind = name.split('-')
        if kind != 'bytes':
            # Skip object stats -- they're not very useful.
            continue
        footprint.append((section, vals))
    footprint.sort()
    
    print('Arithmetic operations:')
    showstatblock(ops_arith, 'ops')
    print()
    print('Memory accesses:')
    showstatblock(ops_mem, 'accesses')
    print()
    print('Footprint:')
    showstatblock(footprint, 'byte-ms')

if __name__ == '__main__':
    args = sys.argv[1:]
    if args:
        files = args
    else:
        files = [DEFAULT_FILENAME]
    
    for fn in files:
        with open(fn) as f:
            stats = json.load(f)
        showstats(stats)
