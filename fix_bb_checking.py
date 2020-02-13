#!/usr/bin/python

import sys
import xml.etree.ElementTree as ET

strInput = ''

for line in sys.stdin:
	strInput += line

e = ET.fromstring(strInput.replace("US-ASCII", "ISO-8859-1"))

for trn in e.iter('STMTTRN'):
	if trn.find('CHECKNUM') != None:
		trn.remove(trn.find('CHECKNUM'))


#e.write(sys.argv[1].split('.')[0]+'_fixed.ofx', encoding="UTF-8")

ET.ElementTree(e).write('extrato_fixed.ofx', encoding="UTF-8")

