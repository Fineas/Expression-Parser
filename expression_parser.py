import string
from pwn import *
from termcolor import colored

# ==============
# environment
# ==============
constants = string.uppercase
log_con = '!' # not
log_con += '&' # and
log_con += '|' # or
log_con += '>' # implication
log_con += '~' # equivalence
EXP = ''
sentences = []
depth = 0

# =============
# subroutines
# =============
def banner():
    print '='*20
    print colored('Expression Parser', 'cyan', attrs=['bold'])
    print '='*20


def parse_expression(payload):
    global constants
    global log_con
    global sentences
    global depth
    if len(payload) == 1:
        if payload[0] in constants:
            print payload,'is an ATOM'
            print '['+colored('*','green')+'] Valid Expression :)'
            return
        else:
            print payload,'is an invalid ATOM'
            print '['+colored('*','red')+'] Invalid Expression'
            return
    if len(payload) < 4:
        print 'The smallest Sentence, bigger than an Atom, has at least 4 characters (ex. '+colored('(!Q)','blue')+' )'
        print '['+colored('*','red')+'] Invalid Expression'
        return
    else:
        # chr holds one character at a time, counter holds the current idx
        for chr,counter in zip( payload , range(len(payload)) ):
            print '['+colored('#','yellow')+'] Testing',payload[:counter]+colored(payload[counter],'red')+payload[counter+1:]
            # ==================
            # DEBUG PURPOSE
            # print chr,'|',counter
            # print sentences
            # ==================
            # if character is an open PARANTHESIS
            if chr == '(':
                if payload[counter+1] == '!':
                    print '\t['+colored('!','magenta')+'] New negation Sentence\n'
                    sentences.append([False, False]) # negation sentence
                    depth += 1
                elif payload[counter+1] in constants:
                    print '\t['+colored('!','magenta')+'] New Sentence\n'
                    sentences.append([False,False,False])
                    depth += 1
                elif payload[counter+1] == '(':
                    print '\t['+colored('!','magenta')+'] New Sentence\n'
                    sentences.append([False, False, False])
                    depth += 1
                else:
                    print '\t['+colored('!','magenta')+'] Character ( can only be followed by ! or another (\n'
                    print '['+colored('*','red')+'] Invalid Expression'
                    return
            # if character is a CONSTATN
            elif chr in constants:
                if counter < len(payload)-1 :
                    if payload[counter-1] in log_con: # this means variable is on right side
                        if payload[counter+1] == ')':
                            if payload[counter-1] == '!':
                                sentences[depth-1][1] = True
                                print '\t['+colored('!','magenta')+'] Variable is on the RIGHT side of the Negation Sentence\n'
                            else:
                                sentences[depth-1][2] = True
                                print '\t['+colored('!','magenta')+'] Variable is on the RIGHT side of the Sentence\n'
                        else:
                            print '['+colored('*','red')+'] Invalid Expression'
                            return
                    elif payload[counter+1] in log_con: # this means variable is on left side
                        if payload[counter-1] == '(':
                            if payload[counter+1] != '!':
                                print '\t['+colored('!','magenta')+'] Variable is on the LEFT side of the Sentence\n'
                                sentences[depth-1][0] = True # first part of sentence is valid
                            else:
                                print '\t['+colored('!','magenta')+'] Invalid syntax, a Variable cannot be followed by !\n'
                                print '['+colored('*','red')+'] Invalid Expression' # we cannot have syntax: A!
                                return
                        else:
                            print '['+colored('*','red')+'] Invalid Expression'
                            return
                    else:
                        print '\t['+colored('!','magenta')+'] A Variable can only be followed by a Logical Connection or a (\n'
                        print '['+colored('*','red')+'] Invalid Expression'
                        return
                else:
                    print '\t['+colored('!','magenta')+'] A Variable cannot be placed at the end of an Expression.\n'
                    print '['+colored('*','red')+'] Invalid Expression'
                    return
            # if character is a CONNECTOR
            elif chr in log_con:
                if chr == '!':
                    if payload[counter-1] == '(':
                        if payload[counter+1] == '(' or payload[counter+1] in constants:
                            print '\t['+colored('!','magenta')+'] The Logical Connection is placed at the begining of the sentence\n'
                            sentences[depth-1][0] = True
                        else:
                            print '\t['+colored('!','magenta')+'] The Logical Connection ! is only following a Variable or a (\n'
                            print '['+colored('*','red')+'] Invalid Expression' # we cannot have something different but ( or CONST after !
                            return
                    else:
                        print '\t['+colored('!','magenta')+'] The Logical Connection ! can only be followed by a (\n'
                        print '['+colored('*','red')+'] Invalid Expression' # we cannot have something different but ( before !
                        return
                else:
                    if payload[counter-1] in constants and payload[counter+1] in constants: # we can have A # A
                        sentences[depth-1][1] = True
                        print '\t['+colored('!','magenta')+'] The Logical Connection is between two Variables\n'
                    elif payload[counter-1] in constants and payload[counter+1] == '(': # we can have A # (
                        sentences[depth-1][1] = True
                        print '\t['+colored('!','magenta')+'] The Logical Connection is between a Variables and a (\n'
                    elif payload[counter-1] == ')' and payload[counter+1] in constants: # we can have ) # A
                        sentences[depth-1][1] = True
                        print '\t['+colored('!','magenta')+'] The Logical Connection is between one ) and a Variable\n'
                    elif payload[counter-1] == ')' and payload[counter+1] == '(': # we can have ) # (
                        sentences[depth-1][1] = True
                        print '\t['+colored('!','magenta')+'] The Logical Connection is between two Parenthesis\n'
                    else:
                        print '['+colored('*','red')+'] Invalid Expression' # any other combination is wrong
                        return
            # if character is a closed PARANTHESIS
            elif chr == ')':
                if payload[counter-1] in constants or payload[counter-1] == ')':
                    tmp_len = len(sentences[depth-1])
                    flag = 1
                    for i in range(tmp_len):
                        if sentences[depth-1][i] != True:
                            flag = 0
                    if flag:
                        sentences.pop() # remove the current sentence from the list
                        depth -= 1 # get back to the previous sentence
                        #set subject to True from previous sentence
                        if sentences:
                            if len(sentences[depth-1]) == 2: # if it's a negation sentence, set the only variable to True
                                sentences[depth-1][1] = True
                                print '\t['+colored('!','magenta')+'] End of a Valid Sentence.\n'
                            else:
                                if sentences[depth-1][0]: # if first variable of sentence is True then we set the second variable to true
                                    sentences[depth-1][2] = True
                                    print '\t['+colored('!','magenta')+'] End of a Valid Sentence.\n'
                                else: # if it is not, we will set it to true
                                    sentences[depth-1][0] = True
                                    print '\t['+colored('!','magenta')+'] End of a Valid Sentence.\n'
                        elif counter < len(payload)-1:
                            continue
                        else:
                            print '['+colored('*','green')+'] Valid Expression :)'
                            return
                    else:
                        print '\t['+colored('!','magenta')+'] End of Invalid Sentence.\n'
                        print '['+colored('*','red')+'] Invalid Expression'
                        return
                else:
                    print '\t['+colored('!','magenta')+'] End of Invalid Sentence.\n'
                    print '['+colored('*','red')+'] Invalid Expression'
                    return

            # invalid character
            else:
                print 'Unknown character',i
                print '['+colored('*','red')+'] Invalid Expression'
                return

# ============
# MAIN
# ============
if __name__ == "__main__":
    banner()
    global EXP
    EXP = raw_input('> ').strip() # Read Input
    parse_expression(EXP) # Parse Input
