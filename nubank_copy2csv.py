#!/usr/bin/python
# -*- coding: latin_1 -*-

import sys

# constants
NAME = 0
INT = 1
PERIOD = 2
COMMA = 3
AMNT = 4
FSLASH = 5
ASTRSK = 6
COLON = 7
DOLLAR = 8
HYPHEN = 9
LNBRK = 49
OTHER = 50


sym = ''
ident = ''

ch = ''

year = '2018'
result = ''


#scanner

def isBlank (char):
    acceptableChars = [' ', '\t', '\r', '']
    if char in acceptableChars:
        return True
    
    return False
    
def isLetter (char):
    if (char != '') and (char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÁÉÍÓÚáéíóúÀÈÌÒÙàèìòùÂÊÎÔÛâêîôûÃÕãõÇç&'):
        return True
        
    return False
    
def isNameChar (char):
    additionalChars = ['-', '*', '/', ':', '$', '%', '#', '.']
    if isLetter (char) or isDigit (char) or char in additionalChars:
        return True
    
    return False
    
def isDigit (char):
    acceptableChars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    if char in acceptableChars:
        return True
    
    return False

def isLineBreak (char):
    if char == '\n':
    	return True

    return False


def textRead ():
    global ch
    textRead.counter += 1
    if textRead.counter >= len(textRead.string):
        textRead.eof = True
        ch = ''
    else:
        ch = textRead.string[textRead.counter] 
textRead.counter = -1
textRead.line = 1

f = open (sys.argv[1], 'r')
#f = open ('raw nubank statement.txt', 'r')
textRead.string = f.read()
f.close ()
textRead.eof = False

def getSym ():
    global sym, ident
    
    sym = ''
    ident = ''
    
    while (not textRead.eof) and (isBlank(ch)):
        textRead ()  # skip blanks
    
    if isDigit (ch):
        sym = INT
    elif isNameChar (ch):
        sym = NAME
    elif ch == ',':
        sym = COMMA
        ident = ','
        textRead ()
        return
    elif isLineBreak (ch):
        sym = LNBRK
	textRead.line += 1
        textRead ()
        return
    else:
        sym = OTHER
        textRead ()
        return
    
    while True:
        if sym == INT:
            ident += ch
            textRead ()
            if not isDigit (ch):
                if ch == '.':
                    textRead ()
                    continue
                elif (ch == ','):
                    sym = AMNT
                    continue
                elif isNameChar (ch):
                    sym = NAME
                    continue
                break
        if sym == AMNT:
            ident += ch
            textRead ()
            if not isDigit (ch):
                if isNameChar (ch):
                    ident = ident.replace(',', '.')
                    sym = NAME
                    continue
                break
        if sym == NAME:
            ident += ch
            textRead ()
            if not (isNameChar (ch) or ch == '.'):
                break 



#parser

def error (string):
    print (string)
    print ('Halted at line: ' + str(textRead.line))
    print ('Result so far: ' + result)
    print ('Current token identifier: ' + ident)
    print ('Contents of input position: ' + textRead.string[textRead.counter:textRead.counter+5])
    exit ()

def date ():  #Adds directly to the global variable 'result'
    global result
    
    if sym == INT:
        result += ident + '/'
        getSym ()
    else:
        error ('Error: integer expected to form a date, got type ' + str(sym) + ' instead at input position ' + str(textRead.counter))
    month()
    result += year + ','
    
def month ():
    global result
    
    allowedMonths = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
    
    if (sym == NAME) and (ident.lower() in allowedMonths):
        for i in range (0, 12):
            if ident.lower() == allowedMonths[i]:
                result += str(i+1) + '/'
                break
        getSym ()
    else:
        error ('Error: month expected, got type ' + str(sym) + ' instead')

def memo ():
    returnValue = ''
    
    if (sym != LNBRK):
        returnValue += ident
        getSym ()
    else:
        error ('Error: identifier or integer expected, got type ' + str(sym) + ' instead')
    while (sym != LNBRK):
        returnValue += ' ' + ident
        getSym ()
        
    return returnValue
    
    
def type ():
    returnValue = ''
    
    if (sym == NAME):
        returnValue = ident
        getSym ()
   
    while (sym != LNBRK):
        returnValue += ' ' + ident
        getSym ()
    
    return returnValue

def lnBrk ():
    if (sym != LNBRK):
        error ('Error: line break expected, got type ' + str(sym) + ' instead')
    getSym ()

def trnAmnt ():
    returnValue = ''

    if (sym != NAME) or (ident != 'R$'):
        error ('Error: \'R$\' expected, got ' + ident + ' instead')
    getSym()

    if (sym != AMNT):
        error ('Error: amount expected, got type ' + str(sym) + ' instead at input position ' + srt(textReader.counter))
    returnValue += ident.replace(',','.')
    getSym()

    return returnValue

def fgnTrnAmnt ():
    returnValue = ''
    currSymb = ident
    getSym()

    if (sym != AMNT):
        error ('Error: amount expected, got type ' + str(sym) + ' instead at input position ' + srt(textReader.counter))
    returnValue += ident.replace(',','.') + ' ' + currSymb
    getSym()

    return returnValue


def transaction ():
    global result

    partialResult = ''
    memoText = ''
    trnAmntText = ''
    category = ''

    while (sym == LNBRK):
        getSym()
    
    category = type ()
    if (category == 'Fatura paga'):
        lnBrk ()
        getSym ()
	getSym ()
	lnBrk ()
	return
    if (category == 'Pagamento recebido'):
        lnBrk ()
        trnAmntText = trnAmnt ()
        lnBrk ()
        date ()
        result += ',' + ',' + category + ',' + ',' + trnAmntText + '\n'
        getSym()
        return

    lnBrk ()    
    memoText = memo ()
    lnBrk ()
    trnAmntText = trnAmnt ()
    lnBrk ()

    if (sym == NAME):
        memoText += ' ' + fgnTrnAmnt ()
        lnBrk ()
    
    date() #Adds directly to the global variable

    result += ',' + ',' + memoText + ',' + trnAmntText  + ',\n'

    getSym()
    
  
def parse ():
    getSym ()
    transaction ()
    while not textRead.eof:
        transaction ()
        

result += 'Date,Payee,Category,Memo,Outflow,Inflow\n'
parse ()
f = open (sys.argv[1].replace('txt', 'csv'), 'w')
f.write (result)
f.close ()
