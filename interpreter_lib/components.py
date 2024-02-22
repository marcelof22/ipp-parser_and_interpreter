#author: Marcel Feiler
#project: IPP - 2 (ippcode23)
#FIT VUT BR


import xml.etree.ElementTree as ET
import re
from interpreter_lib.instructions import Instruction
from interpreter_lib.instruction_list import InstructionList
from interpreter_lib.exit_codes import *
import sys




class Xml():
    def __init__(self, xml_file):
        super().__init__()
        self.XMLpath = xml_file

    def check_integrity_of_tree(self):
        try:
            if self.XMLpath != 'sys.stdin' :
                myTree = ET.parse(self.XMLpath)
            else:
                myTree = ET.parse(sys.stdin)

        except FileNotFoundError:
            exit(ExitCodes.inFileError)

        except Exception:
            exit(ExitCodes.xmlError)

        try:
            self.root = myTree.getroot()
        except:
            exit(ExitCodes.xmlError)


        try:
            #checking header ippcode23
            if ('language' not in self.root.attrib) and (not re.match('^ippcode23$', self.root.attrib['language'], re.IGNORECASE)): #CHANGE!!!
                exit(ExitCodes.syntaxError)
        except KeyError:
                exit(ExitCodes.xmlError)

        
    def check_each_instruction(self):
        my_order = 0
        possible_datatypes = ['int', 'bool', 'string', 'label', 'var', 'type', 'nil']

        for child in self.root:
            arg_n = 0
            #checking instruction tag
            if child.tag != 'instruction':
                exit(ExitCodes.syntaxError)

            #checking order and opcode tags
            if ('order' not in child.attrib) or ('opcode' not in child.attrib) or (len(child.attrib) != 2):
                exit(ExitCodes.syntaxError)

            try:
                index_tmp = int(child.attrib['order'])
                instr_n = index_tmp
            except ValueError:
                exit(ExitCodes.syntaxError)

            if instr_n <= my_order or instr_n < 1:
                exit(ExitCodes.syntaxError)

            for arg in child:
                arg_n += 1
                if arg.tag != 'arg' + str(arg_n) :
                    exit(ExitCodes.syntaxError)
                if 'type' not in arg.attrib:
                    exit(ExitCodes.syntaxError)
                if arg.attrib['type'] not in possible_datatypes:
                    exit(ExitCodes.syntax)
    
    def instruction_importing(self, in_list:InstructionList):
        no_args = ['CREATEFRAME', 'PUSHFRAME', 'POPFRAME', 'BREAK', 'RETURN']
        one_arg = ['DPRINT', 'DEFVAR', 'CALL', 'PUSHS', 'POPS', 'LABEL', 'JUMP', 'WRITE', 'EXIT'] 
        two_args = ['MOVE', 'INT2CHAR', 'READ', 'STRLEN', 'TYPE', 'NOT']
        three_args = ['ADD', 'SUB', 'MUL', 'IDIV', 'LT', 'GT', 'EQ', 'AND', 'OR', 'JUMPIFEQ', 'JUMPIFNEQ', 'STRI2INT', 'CONCAT', 'GETCHAR', 'SETCHAR']

        #separating instruction by number of args
        for inst in self.root:
            actual_inst = inst.attrib['opcode'].upper()
            if actual_inst in no_args :
                self.arg_check(0, inst)
                i = Instruction(actual_inst) 
                in_list.instruction_insert(i)
            elif actual_inst in one_arg :
                self.arg_check(1, inst)
                i = Instruction(actual_inst, inst[0]) 
                in_list.instruction_insert(i)
            elif actual_inst in two_args :
                self.arg_check(2, inst)
                i = Instruction(actual_inst, inst[0], inst[1]) 
                in_list.instruction_insert(i)
            elif actual_inst in three_args :
                self.arg_check(3, inst)
                i = Instruction(actual_inst, inst[0], inst[1], inst[2]) 
                in_list.instruction_insert(i)
            else :
                exit(ExitCodes.syntaxError)        
            
    def arg_check(self, amount, instruction):
        if (len(list(instruction))) != amount:
            exit(ExitCodes.syntaxError)

   