import argparse
from anytree import *
import string
from termcolor import colored

# ==============
# environment
# ==============
constants = string.uppercase+'1'+'0'
log_con = '!' # not
log_con += '&' # and
log_con += '|' # or
log_con += '>' # implication
log_con += '~' # equivalence

EXP = ''
var_name = []
var_values = []
depth = 0
root = 0
prev = 0
valid = 1
exp_value = []
arrays = []
final = False

# =============
# subroutines
# =============

def xor(x,y):
    return (((not y) and x) or ((not x) and y))

func_not = lambda x : not x
#print func_not(True)
#print func_not(False)

func_and = lambda x,y : x&y
# print func_and(True,True) == True
# print func_and(True,False) == False
# print func_and(False,True) == False
# print func_and(False,False) == False

func_or = lambda x,y : x|y
# print func_or(True,True) == True
# print func_or(True,False) == True
# print func_or(False,True) == True
# print func_or(False,False) == False

func_impl = lambda x,y : ((not x) or y)
# print func_impl(True,True) == True
# print func_impl(True,False) == Flase
# print func_impl(False,True) == True
# print func_impl(False,False) == True

func_equ = lambda x,y : not xor(x,y)
# print func_equ(True,True)
# print func_equ(True,False)
# print func_equ(False,True)
# print func_equ(False,False)

# exaple: [[P,>,[!,[!,[!,[!,[!,B]]]]]],~,[Q,&,S]]
def parse_list():
    global var_name
    global constants

    input = raw_input('['+colored('>','blue')+'] Enter the abstract syntax for the sentence:')
    input = input.strip()
    input = input.replace(',','')
    input = input.replace('[','(')
    input = input.replace(']',')')

    for i in input:
        if (i in constants) and (i not in var_name):
            var_name.append(i)

    print '['+colored('*','red')+'] SENTENCE:',input
    return input

def banner():
    print '='*20
    print colored('Expression Parser', 'cyan', attrs=['bold'])
    print '='*20

def read_expression():
    global constants
    global var_name
    global var_values
    global EXP
    EXP = raw_input('> ').strip() # Read Input

    for i in EXP:
        if (i in constants) and (i not in var_name):
            var_name.append(i)
    print ''

def read_var_values():
    global var_name
    global var_values
    global EXP

    for i in var_name:
        if i == '1':
            var_values.append(True)
        elif i == '0':
            var_values.append(False)
        else:
            var_values.append(eval(raw_input('['+colored('>','yellow')+'] Enter value for '+colored(str(i),'green')+' (True/False): ').strip()))
            if var_values[len(var_values)-1] == True or var_values[len(var_values)-1] == False:
                continue
            else:
                print '['+colored('!!','red')+'] Invalid Value'
                exit(0)
            print ''

def print_tree():
    global root

    print '-'*30
    print '['+colored('#','blue')+'] TREE REPRESENTATION'
    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name))
    print '-'*30

def generate_picture():
    global root

    from anytree.exporter import DotExporter
    DotExporter(root).to_picture("./exp_tree.png")

def validate(debug=1):
    global EXP
    global var_name
    global var_values
    global log_con
    global depth
    global root
    global prev
    global valid
    global exp_value
    global final

    # if the expression is an Atom
    if len(EXP) == 1:
        if EXP[0] in var_name:
            if debug:
                print EXP,'is an ATOM'
                print '-'*30
                print '['+colored('*','green')+'] Well Fromed Expression :)'
            return
        else:
            if debug:
                print EXP,'is an invalid ATOM'
                print '-'*30
                print '['+colored('*','red')+'] Not Well Formed Sentence\n'
            valid = 0; return
    # invalid length for a valid expression
    elif len(EXP) < 4:
        if debug:
            print 'The smallest Sentence, bigger than an Atom, has at least 4 characters (ex. '+colored('(!Q)','blue')+' )'
            print '-'*30
            print '['+colored('*','red')+'] Not Well Formed Sentence\n'
        valid = 0; return
    # do the real parse
    else:
        root = None
        prev = None
        for chr,counter in zip( EXP , range(len(EXP)) ):
            if debug:
                print '['+colored('#','yellow')+'] Testing',EXP[:counter]+colored(EXP[counter],'red')+EXP[counter+1:]
            # ==================
            # DEBUG PURPOSE
            # print chr,'|',counter
            # print sentences
            # ==================
            if chr == '(':
                if EXP[counter+1] == '!':
                    if debug:
                        print '\t['+colored('!','magenta')+'] New negation Sentence\n'
                    ########### this is for the expression array #########
                    exp_value.append([None, None]) # negation sentence
                    depth += 1
                    if root:
                        tmp_node = Node('',parent=prev)
                        prev = tmp_node
                    else:
                        root = Node('')
                        prev = root
                elif EXP[counter+1] in constants:
                    if debug:
                        print '\t['+colored('!','magenta')+'] New Sentence\n'
                    ########### this is for the expression array #########
                    exp_value.append([None, None, None]) # sentence
                    depth += 1
                    if root:
                        tmp_node = Node('',parent=prev)
                        prev = tmp_node
                    else:
                        root = Node('')
                        prev = root
                elif EXP[counter+1] == '(':
                    if debug:
                        print '\t['+colored('!','magenta')+'] New Sentence\n'
                    ########### this is for the expression array #########
                    exp_value.append([None, None, None]) # sentence
                    depth += 1
                    if root:
                        tmp_node = Node('',parent=prev)
                        prev = tmp_node
                    else:
                        root = Node('')
                        prev = root
                else:
                    if debug:
                        print '\t['+colored('!','magenta')+'] Character ( can only be followed by ! or another (\n'
                        print '-'*30
                        print '['+colored('*','red')+'] Not Well Formed Sentence\n'
                    valid = 0; return
            # ============================
            # Handle constants (variables)
            # ============================
            elif chr in var_name:
                if counter < len(EXP)-1 :
                    if EXP[counter-1] in log_con: # this means variable is on right side
                        if EXP[counter+1] == ')':
                            if EXP[counter-1] == '!':
                                exp_value[depth-1][1] = var_values[var_name.index(chr)]
                                tmp_node = Node(chr,parent=prev)
                                if debug:
                                    print '\t['+colored('!','magenta')+'] Variable is on the RIGHT side of the Negation Sentence\n'
                            else:
                                exp_value[depth-1][2] = var_values[var_name.index(chr)]
                                tmp_node = Node(chr,parent=prev)
                                if debug:
                                    print '\t['+colored('!','magenta')+'] Variable is on the RIGHT side of the Sentence\n'
                        else:
                            if debug:
                                print '-'*30
                                print '['+colored('*','red')+'] Not Well Formed Sentence\n'
                            valid = 0; return
                    elif EXP[counter+1] in log_con: # this means variable is on left side
                        if EXP[counter-1] == '(':
                            if EXP[counter+1] != '!':
                                if debug:
                                    print '\t['+colored('!','magenta')+'] Variable is on the LEFT side of the Sentence\n'
                                exp_value[depth-1][0] = var_values[var_name.index(chr)]
                                tmp_node = Node(chr,parent=prev) # first part of sentence is valid
                            else:
                                if debug:
                                    print '\t['+colored('!','magenta')+'] Invalid syntax, a Variable cannot be followed by !\n'
                                    print '-'*30
                                    print '['+colored('*','red')+'] Not Well Formed Sentence\n' # we cannot have syntax: A!
                                valid = 0; return
                        else:
                            if debug:
                                print '-'*30
                                print '['+colored('*','red')+'] Not Well Formed Sentence\n'
                            valid = 0; return
                    else:
                        if debug:
                            print '\t['+colored('!','magenta')+'] A Variable can only be followed by a Logical Connection or a (\n'
                            print '-'*30
                            print '['+colored('*','red')+'] Not Well Formed Sentence\n'
                        valid = 0; return
                else:
                    if debug:
                        print '\t['+colored('!','magenta')+'] A Variable cannot be placed at the end of an Expression.\n'
                        print '-'*30
                        print '['+colored('*','red')+'] Not Well Formed Sentence\n'
                    valid = 0; return
            # ============================
            # if character is a CONNECTOR
            # ============================
            elif chr in log_con:
                if chr == '!':
                    if EXP[counter-1] == '(':
                        if EXP[counter+1] == '(' or EXP[counter+1] in var_name:
                            if debug:
                                print '\t['+colored('!','magenta')+'] The Logical Connection is placed at the begining of the sentence\n'
                            exp_value[depth-1][0] = chr
                            prev.name = chr
                        else:
                            if debug:
                                print '\t['+colored('!','magenta')+'] The Logical Connection ! is only following a Variable or a (\n'
                                print '-'*30
                                print '['+colored('*','red')+'] Not Well Formed Sentence\n' # we cannot have something different but ( or CONST after !
                            valid = 0; return
                    else:
                        if debug:
                            print '\t['+colored('!','magenta')+'] The Logical Connection ! can only be followed by a (\n'
                            print '-'*30
                            print '['+colored('*','red')+'] Not Well Formed Sentence\n' # we cannot have something different but ( before !
                        valid = 0; return
                else:
                    if EXP[counter-1] in var_name and EXP[counter+1] in var_name: # we can have A # A
                        exp_value[depth-1][1] = chr
                        prev.name = chr
                        if debug:
                            print '\t['+colored('!','magenta')+'] The Logical Connection is between two Variables\n'
                    elif EXP[counter-1] in var_name and EXP[counter+1] == '(': # we can have A # (
                        exp_value[depth-1][1] = chr
                        prev.name = chr
                        if debug:
                            print '\t['+colored('!','magenta')+'] The Logical Connection is between a Variables and a (\n'
                    elif EXP[counter-1] == ')' and EXP[counter+1] in var_name: # we can have ) # A
                        exp_value[depth-1][1] = chr
                        prev.name = chr
                        if debug:
                            print '\t['+colored('!','magenta')+'] The Logical Connection is between one ) and a Variable\n'
                    elif EXP[counter-1] == ')' and EXP[counter+1] == '(': # we can have ) # (
                        exp_value[depth-1][1] = chr
                        prev.name = chr
                        if debug:
                            print '\t['+colored('!','magenta')+'] The Logical Connection is between two Parenthesis\n'
                    else:
                        if debug:
                            print '-'*30
                            print '['+colored('*','red')+'] Not Well Formed Sentence\n' # any other combination is wrong
                        valid = 0; return
            # ===================================== ==============
            # if character is a closed PARANTHESIS + interpretate
            # ===================================== ==============
            elif chr == ')':
                if prev == None:
                    if debug:
                        print '\t['+colored('!','magenta')+'] Too many ) characters\n'
                        print '-'*30
                        print '['+colored('*','red')+'] Not Well Formed Sentence\n' # any other combination is wrong
                    valid = 0; return
                if EXP[counter-1] in var_name or EXP[counter-1] == ')':
                    if prev.name == '!':
                        if len(prev.children) == 1:
                            prev = prev.parent
                            result = func_not(exp_value[depth-1][1])
                            if len(exp_value[depth-2]) == 3:
                                if exp_value[depth-2][0] == None:
                                    exp_value[depth-2][0] = result
                                else:
                                    exp_value[depth-2][2] = result
                            elif len(exp_value[depth-2]) == 2:
                                if exp_value[depth-2][1] == None:
                                    exp_value[depth-2][1] = result
                            else:
                                if debug:
                                    print '-'*30
                                    print '['+colored('*','red')+'] Not Well Formed Sentence\n'
                                valid = 0; return
                            depth -= 1
                            tmp_pop = exp_value.pop()
                            if not exp_value:
                                final = result
                            if debug:
                                print '\t['+colored('!','magenta')+'] End of a Valid Sentence.\n'
                        else:
                            if debug:
                                print '\t['+colored('!','magenta')+'] End of Invalid Sentence.\n'
                                print '-'*30
                                print '['+colored('*','red')+'] Not Well Formed Sentence\n'
                            valid = 0; return
                    elif prev.name in log_con:
                        if len(prev.children) == 2:
                            prev = prev.parent
                            # calculate value
                            if exp_value[depth-1][1] == '&':
                                result = func_and(exp_value[depth-1][0],exp_value[depth-1][2])
                            elif exp_value[depth-1][1] == '|':
                                result = func_or(exp_value[depth-1][0],exp_value[depth-1][2])
                            elif exp_value[depth-1][1] == '>':
                                result = func_impl(exp_value[depth-1][0],exp_value[depth-1][2])
                            else:
                                result = func_equ(exp_value[depth-1][0],exp_value[depth-1][2])
                            # replace value
                            if len(exp_value[depth-2]) == 3:
                                if exp_value[depth-2][0] == None:
                                    exp_value[depth-2][0] = result
                                else:
                                    exp_value[depth-2][2] = result
                            elif len(exp_value[depth-2]) == 2:
                                exp_value[depth-2][1] = result
                            else:
                                if debug:
                                    print '-'*30
                                    print '['+colored('*','red')+'] Not Well Formed Sentence\n'
                                valid = 0; return
                            depth -= 1
                            tmp_pop = exp_value.pop()
                            if not exp_value:
                                final = result
                            if debug:
                                print '\t['+colored('!','magenta')+'] End of a Valid Sentence.\n'
                        else:
                            if debug:
                                print '\t['+colored('!','magenta')+'] End of Invalid Sentence.\n'
                                print '-'*30
                                print '['+colored('*','red')+'] Not Well Formed Sentence\n'
                            valid = 0; return
                    else:
                        if debug:
                            print '-'*30
                            print '['+colored('*','red')+'] Not Well Formed Sentence\n'
                        valid = 0; return

            # invalid character
            else:
                if debug:
                    print 'Unknown character',i
                    print '-'*30
                    print '['+colored('*','red')+'] Not Well Formed Sentence\n'
                valid = 0; return

            if debug:
                print '['+colored('#','yellow')+'] Status:',exp_value
    if exp_value:
        if debug:
            print '['+colored('*','red')+'] Not Well Formed Sentence\n'
        valid = 0; return

def scoate(v):
    global arrays
    if v not in arrays:
        arrays.append(v)
    for child in v:
        if type(child) is list:
            scoate(child)

def generate_truth_table():
    global EXP
    global var_name
    global var_values
    global log_con
    global arrays

    save_exp = EXP

    i = 0 # use the flag in order to not repeat the loop
    spl_exp = EXP.replace('(','[').replace(')',']').replace("!","'!',").replace("~",",'~',").replace(">",",'>',").replace("&",",'&',").replace("|",",'|',")
    for i in var_name:
        spl_exp = spl_exp.replace(i,"'"+i+"'")

    spl_exp = eval(spl_exp)
    scoate(spl_exp)

    do_parse = []

    for i in arrays[::-1]:
        do_parse.append(str(i).replace('[','(').replace(']',')').replace(',','').replace("'",'').replace(" ",''))
    #print do_parse

    t_header = ''
    for i in var_name:
        t_header += colored(i,'blue') + ' '*2
    for i in do_parse:
        t_header += colored(i,'blue') + ' '*2

    print '-'*30
    print t_header

    vars = len(var_name)
    payload = '1'*vars
    payload = int('0b'+payload,2)
    while payload != 0:
        t_row = ''
        # initiate variables values
        for i in range(len(var_name)):
            if var_name[i] == '1':
                var_values.append(1)
            elif var_name[i] == '0':
                var_values.append(0)
            else:
                var_values.append(eval(bin(payload)[2:].rjust(vars,'0')[i]))
        # print ROW:
        for i in var_values:
            if i:
                t_row += colored(str(i).ljust(3,' '),'red')
            else:
                t_row += str(i).ljust(3,' ')
        for i in do_parse:
            EXP = i
            validate(0)
            if final:
                t_row += colored(str(eval(str(1))).ljust(len(EXP)+2,' '),'red')
            else:
                t_row += str(eval(str(0))).ljust(len(EXP)+2,' ')
        print t_row
        payload -= 1
        var_values = []

    t_row = ''
    # initiate variables values
    for i in range(len(var_name)):
        if var_name[i] == '1':
            var_values.append(1)
        elif var_name[i] == '0':
            var_values.append(0)
        else:
            var_values.append(eval(bin(payload)[2:].rjust(vars,'0')[i]))
    # print ROW:
    for i in var_values:
        if i:
            t_row += colored(str(i).ljust(3,' '),'red')
        else:
            t_row += str(i).ljust(3,' ')
    for i in do_parse:
        EXP = i
        validate(0)
        if final:
            t_row += colored(str(eval(str(1))).ljust(len(EXP)+2,' '),'red')
        else:
            t_row += str(eval(str(0))).ljust(len(EXP)+2,' ')
    print t_row

    EXP = save_exp

def relax(expression):
    caca = 1
    # TODO

# ============
# MAIN
# ============
if __name__ == "__main__":

    banner()

    parser = argparse.ArgumentParser(description='Expression Parser')
    parser.add_argument('--eval'   , '-e', action="store_true")
    parser.add_argument('--int', '-i', action="store_true")
    parser.add_argument('--tab', '-t', action="store_true")
    parser.add_argument('--rel', '-r', action="store_true")
    parser.add_argument('--tree', '-tr', action="store_true")
    parser.add_argument('--png', '-p', action="store_true")
    args = parser.parse_args()

    # ========
    # Program will convert from the relaxed syntax to complete syntax
    if args.rel:
        # TODO
        not_implemented_yet = 1

    # ========
    # Program will only tell if the Expression is Well Formed or not
    if args.eval:
        read_expression()
        validate()
        if valid:
            print '-'*30
            print '['+colored('*','green')+'] Well Formed Sentence'

    # ========
    # Program will first evaluate the Expression and then Interpretate it's Value
    if args.int:
        if not EXP:
            read_expression()
        read_var_values()
        validate(0)
        if valid:
            print '-'*30
            print '['+colored('SENTENCE INTERPRETATION','green')+']',final

    # ========
    # Program will generate the Truth Table
    if args.tab:
        if EXP:
            generate_truth_table()
        else:
            read_expression()
            generate_truth_table()

    # ========
    # The Program will Generate the Expression Tree
    if args.tree:
        if EXP:
            validate(0)
            if valid:
                print_tree()
            else:
                print '-'*30
                print '['+colored('*','red')+'] Not Well Formed Sentence'
        else:
            read_expression()
            validate(0)
            if valid:
                print_tree()
            else:
                print '-'*30
                print '['+colored('*','red')+'] Not Well Formed Sentence'

    # ========
    # The Program will Generate the Expession Tree and map it to a PNG
    if args.png:
        if EXP:
            validate(0)
            if valid:
                generate_picture()
            else:
                print '-'*30
                print '['+colored('*','red')+'] Not Well Formed Sentence'
        else:
            read_expression()
            validate(0)
            if valid:
                generate_picture()
            else:
                print '-'*30
                print '['+colored('*','red')+'] Not Well Formed Sentence'

    # ========
    # HELP
    if not (args.rel or args.eval or args.int or args.tab or args.tree or args.png):
        out = 'usage: expression_interpreter.py\n'
        out += '[-h] (this message) \n'
        out += '[--eval] (evaluate expression)\n'
        out += '[--int] (interpretate expression)\n'
        out += '[--tab] (generate truth table)'
        out += '[--rel] (relaxed syntax)\n'
        out += '[--tree] (prin tree view)\n'
        out += '[--png] (map tree view to a png)\n'
        print out

    # EXP = parse_list()




# ================
#  TESTS
# ================
'''
1. (((P>Q)|S)~T)
2. (P>(Q&(S>T))))
3. (!(B(!Q))&R)
4. (P&((!Q)&(!(!(F~(!R))))))
5. (P|Q)>!(P|Q))&(P|(!(!Q)))
'''
