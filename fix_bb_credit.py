#!/usr/bin/python

import sys
import xml.etree.ElementTree as ET

strInput = ''

for line in sys.stdin:
	strInput += line

e = ET.fromstring(strInput.replace("US-ASCII", "ISO-8859-1"))

for trn in e.iter('STMTTRN'):
	if trn.find('CURRENCY') != None:
		memo = trn.find('MEMO').text
		amnt = trn.find('TRNAMT').text
		amntfloat = float(amnt)
		cursymb = trn.find('CURRENCY').find('CURSYM').text
		trn.find('MEMO').text = memo + " $" + str(abs(amntfloat)) + " " + cursymb
		rate = float(trn.find('CURRENCY').find('CURRATE').text)
		oldamnt = float(trn.find('TRNAMT').text)
		trn.find('TRNAMT').text = str(rate*oldamnt)


#e.write(sys.argv[1].split('.')[0]+'_fixed.ofx', encoding="UTF-8")

ET.ElementTree(e).write('ourocard_fixed.ofx', encoding="UTF-8")

