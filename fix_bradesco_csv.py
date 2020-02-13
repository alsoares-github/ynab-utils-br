#!/usr/bin/python
# -*- coding: latin_1 -*-

import sys
import csv
import datetime


year='2020'
now = datetime.datetime.now()
if now.year != int(year):
    print('Warning: year has changed.')

# Open source file
if len(sys.argv) < 2:
    sys.exit('Error: no source file given.')

f = open(sys.argv[1], 'r', encoding='latin-1')
rdr = csv.reader(f, delimiter=';')

# Open destination file for writing
d = open('bradesco_fixed.csv', 'w')
wrt = csv.writer(d, delimiter=',')
wrt.writerow(['Date','Payee','Category','Memo','Outflow','Inflow'])

# Skip rows until 'Data' is found
while True:
    row = next(rdr)
    if len(row) > 0:
        if row[0] == 'Data':
            break

while True:
    row = next(rdr)

    if row[0] == '':
        break

    if 'SALDO ANTERIOR' in row[1]:
        continue

    if '-' not in row[3]:
        wrt.writerow([row[0]+'/'+year,'','', row[1].strip() + (' ' + row[2].replace(',','.') + ' USD' if row[2] != '0,00' else ''), row[3].replace(',','.'), ''])
    else:
        wrt.writerow([row[0]+'/'+year,'','', row[1].strip() + (' ' + row[2].replace(',','.') + ' USD' if row[2] != '0,00' else ''), '', row[3][1:].replace(',','.')])

f.close()
d.close()



    




