#!/usr/bin/python -u

import sys

alldata = []
for line in open(sys.argv[1]).readlines()[3:]:
    spline = line.strip().split()
    date = spline[0]
    rest = ' '.join(spline[1:])
    alldata.append((date, rest))


for i in range(1, 32):
    for line in alldata:
        date, rest = line
        y, m, d = date.split('/')
        newdate = '/'.join([y,m,str(i)])
        print newdate, rest

