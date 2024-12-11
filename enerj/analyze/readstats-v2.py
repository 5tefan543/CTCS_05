#!/usr/bin/env python

import sys
import json

DEFAULT_FILENAME = 'enerjstats.json'

def showstatblock(items, unit='ops'):
    for name, (precise, approx) in items:
        total = precise + approx
        frac = float(approx) / total if total > 0 else 0
        print '  %s: %i %s total, %.1f%% approx' % (name, total, unit, frac * 100)

def showstats(stats):
    for benchmark, data in stats.iteritems():
        print 'Benchmark: %s' % benchmark

        # Display collective noise statistics
        if 'collective' in data:
            print '  Collective Noise Levels:'
            for level, value in enumerate(data['collective']):
                print '    Level %i: %s' % (level, value)

        # Display individual noise statistics
        if 'individual' in data:
            print '  Individual Noise Levels:'
            for const, levels in data['individual'].iteritems():
                print '    %s:' % const
                for level, value in enumerate(levels):
                    print '      Level %i: %s' % (level, value)

        # Display approximateness statistics
        if 'approximateness' in data:
            print '  Approximateness:'
            approximateness = []
            for category, (precise, approx) in data['approximateness'].iteritems():
                approximateness.append((category, (precise, approx)))
            approximateness.sort()  # Sort categories for consistent display
            showstatblock(approximateness, unit="ops")

        print  # Blank line between benchmarks

if __name__ == '__main__':
    args = sys.argv[1:]
    if args:
        files = args
    else:
        files = [DEFAULT_FILENAME]

    for fn in files:
        try:
            with open(fn) as f:
                stats = json.load(f)
            showstats(stats)
        except IOError:
            print 'Error: File "%s" not found.' % fn
        except ValueError as e:
            print 'Error: Failed to parse JSON in file "%s".' % fn
            print 'Details:', e
