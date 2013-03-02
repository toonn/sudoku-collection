#!/usr/bin/env python

import os

dirs = os.listdir('sudoku')
dircounts = [len(os.listdir(os.path.join('sudoku', dir))) for dir in dirs]
dircounts = [str(dc) for dc in dircounts]

padding = ' | '
longitude = [len(dir) for dir in dirs] + [len(dc) for dc in dircounts]
longest = max(longitude)
width = 80 / longest - 2

dirs = [dir.ljust(longest) for dir in dirs]
dircounts = [dc.center(longest) for dc in dircounts]

dirs = [dirs[i:i+width] for i in xrange(0, len(dirs), width)]
dircounts = [dircounts[i:i+width] for i in xrange(0, len(dircounts), width)]

listings = zip(dirs, dircounts)
print '='*(len(padding.join(listings[0][0])))
for listing in listings:
    print padding.join(listing[0])
    print padding.join(listing[1])
    print '='*(len(padding.join(listing[0])))
