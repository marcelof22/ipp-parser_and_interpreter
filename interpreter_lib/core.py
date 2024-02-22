#author: Marcel Feiler
#project: IPP - 2 (ippcode23)
#FIT VUT BR

import sys
import os
from interpreter_lib.components import *
#from interpreter_lib.instruction_list import *
from interpreter_lib.instructions import *
from interpreter_lib.frames import *

class Interpret:

    #controlling operations
    def __init__(self):
        self.sourceXML = ''
        self.sourceInput = ''
        self.__argument_parse()#arguemnts parser

        
    def __argument_parse(self):
        argc = len(sys.argv) # arguments counter
        if argc < 2 or argc > 3:
            exit(ExitCodes.badParameter)

        for arg in sys.argv[1:]:
            if arg.startswith('--source='):
                self.sourceXML = arg[9:]
            elif arg.startswith('--input='):
                self.sourceInput = arg[8:]
            elif (arg == '-h') or (arg == '--help'):
                print('Interpreting code IPPcode23 using basic operations')
                print('--source=file  input XML file with the representation of the source code')
                print('--input=file   file with inputs for interpretation of the source code itself')
                exit(0)
            else:
                exit(ExitCodes.badParameter)

    
    def getXMLPath(self):
        if self.sourceXML == '' :
            return 'sys.stdin'
        return self.sourceXML

    def getInputPath(self):
        return self.sourceInput           
       

    def start(self) :
        #Instruction executing
        #XML storing
        lineCounter = 0
        dataStack = []
        frame = Frames()
        instructionList = InstructionList()

        xml = Xml(self.getXMLPath())    #initialising xml
        xml.check_integrity_of_tree()   #first checking of xml file
        xml.check_each_instruction()    #xml instruction checking
        xml.instruction_importing(instructionList)  #importing instruction to list

        instructionList.string_checking()
        
        #main loop for instructions
        while True:
            #saving required instruction
            act_instruction = instructionList.next_instruction()
        
            #end of instructions
            if act_instruction is None:
                break
            #1
            if act_instruction.type == 'MOVE':
                typy, data = act_instruction.get_data_arg_type(act_instruction.arg2, frame)
                frame.set_var(act_instruction.arg1, typy, data)
            #2
            elif act_instruction.type == 'CREATEFRAME':
                frame.create_frame()
            #3
            elif act_instruction.type == 'PUSHFRAME':
                frame.push_frame()
            #4
            elif act_instruction.type == 'POPFRAME':
                frame.pop_frame()
            #5
            elif act_instruction.type == 'DEFVAR':
                frame.def_var(act_instruction.arg1)
            #6
            elif act_instruction.type == 'CALL':
                instructionList.position_store()
                instructionList.jump(act_instruction.arg1)
            #7
            elif act_instruction.type == 'RETURN':
                instructionList.position_restore()
            #8
            elif act_instruction.type == 'PUSHS':
                typy, data = act_instruction.get_data_arg_type(act_instruction.arg1, frame)
                dataStack.append((typy, data))
            #9
            elif act_instruction.type == 'POPS':
                try:
                    typy, data = dataStack.pop()
                except IndexError:
                    exit(ExitCodes.runErrorMissingValue)

                frame.set_var(act_instruction.arg1, typy, data)
            #10
            elif act_instruction.type == 'ADD':
                type1, data1 = act_instruction.get_data_arg_type(act_instruction.arg2, frame)
                type2, data2 = act_instruction.get_data_arg_type(act_instruction.arg3, frame)

                if type1 == type2 == 'int':
                    frame.set_var(act_instruction.arg1, 'int', str(int(data1)+int(data2)))
                else:
                    exit(ExitCodes.runErrorBadType)
            #11
            elif act_instruction.type == 'SUB':
                type1, data1 = act_instruction.get_data_arg_type(act_instruction.arg2, frame)
                type2, data2 = act_instruction.get_data_arg_type(act_instruction.arg3, frame)

                if type1 == type2 == 'int':
                    frame.set_var(act_instruction.arg1, 'int', str(int(data1)-int(data2)))
                else:
                    exit(ExitCodes.runErrorBadType)
            #12
            elif act_instruction.type == 'MUL':
                type1, data1 = act_instruction.get_data_arg_type(act_instruction.arg2, frame)
                type2, data2 = act_instruction.get_data_arg_type(act_instruction.arg3, frame)

                if type1 == type2 == 'int':
                    frame.set_var(act_instruction.arg1, 'int', str(int(data1)*int(data2)))
                else:
                    exit(ExitCodes.runErrorBadType)
            #13
            elif act_instruction.type == 'IDIV':
                type1, data1 = act_instruction.get_data_arg_type(act_instruction.arg2, frame)
                type2, data2 = act_instruction.get_data_arg_type(act_instruction.arg3, frame)

                if type1 == type2 == 'int':
                    if int(data2) != 0:
                        frame.set_var(act_instruction.arg1, 'int', str(int(data1) // int(data2)))                        
                    else:
                        exit(ExitCodes.runErrorZeroDivision)
                else:
                    exit(ExitCodes.runErrorBadType)
            #14
            elif act_instruction.type == 'LT':
                type1, data1 = act_instruction.get_data_arg_type(act_instruction.arg2, frame)
                type2, data2 = act_instruction.get_data_arg_type(act_instruction.arg3, frame)

                if type1 == type2:
                    if type1 == 'nil' and type2 == 'nil':
                        exit(ExitCodes.runErrorBadType)
                    else:
                        if type1 == 'string':
                            frame.set_var(act_instruction.arg1, 'bool', 'true' if data1 < data2 else 'false')
                        elif type1 == 'nil' :
                            frame.set_var(act_instruction.arg1, 'bool', 'false')
                        elif type1 == 'bool':
                            frame.set_var(act_instruction.arg1, 'bool', 'true' if data1 == 'false' and data2 == 'true' else 'false')
                        else :
                            frame.set_var(act_instruction.arg1, 'bool', 'true' if int(data1) < int(data2) else 'false')
                else:
                    exit(ExitCodes.runErrorBadType)
            #15
            elif act_instruction.type == 'GT':
                type1, data1 = act_instruction.get_data_arg_type(act_instruction.arg2, frame)
                type2, data2 = act_instruction.get_data_arg_type(act_instruction.arg3, frame)

                if type1 == type2:
                    if type1 == 'nil' and type2 == 'nil':
                        exit(ExitCodes.runErrorBadType)
                    else:
                        if type1 == 'string' :
                            frame.set_var(act_instruction.arg1, 'bool', 'true' if data1 > data2 else 'false')
                        elif type1 == 'nil' :
                            frame.set_var(act_instruction.arg1, 'bool', 'false')
                        elif type1 == 'bool':
                            frame.set_var(act_instruction.arg1, 'bool', 'true' if data1 == 'true' and data2 == 'false' else 'false')
                        else :
                            frame.set_var(act_instruction.arg1, 'bool', 'true' if int(data1) > int(data2) else 'false')

                else:
                    exit(ExitCodes.runErrorBadType)
            #16
            elif act_instruction.type == 'EQ':
                type1, data1 = act_instruction.get_data_arg_type(act_instruction.arg2, frame)
                type2, data2 = act_instruction.get_data_arg_type(act_instruction.arg3, frame)

                if type1 == type2:
                    frame.set_var(act_instruction.arg1, 'bool', 'true' if data1 == data2 else 'false')

                elif type1 == 'nil' or type2 == 'nil':
                    frame.set_var(act_instruction.arg1, 'bool', 'false')

                else:
                    exit(ExitCodes.runErrorBadType)
            #17
            elif act_instruction.type == 'AND':
                type1, data1 = act_instruction.get_data_arg_type(act_instruction.arg2, frame)
                type2, data2 = act_instruction.get_data_arg_type(act_instruction.arg3, frame)

                if type1 == type2 == 'bool':
                    frame.set_var(act_instruction.arg1, 'bool', 'true' if data1 == data2 == 'true' else 'false')
                else:
                    exit(ExitCodes.runErrorBadType)
            #18
            elif act_instruction.type == 'OR':
                type1, data1 = act_instruction.get_data_arg_type(act_instruction.arg2, frame)
                type2, data2 = act_instruction.get_data_arg_type(act_instruction.arg3, frame)

                if type1 == type2 == 'bool':
                    frame.set_var(act_instruction.arg1, 'bool', 'true' if data1 == 'true' or data2 == 'true' else 'false')
                else:
                    exit(ExitCodes.runErrorBadType)
            #19
            elif act_instruction.type == 'NOT':
                type1, data1 = act_instruction.get_data_arg_type(act_instruction.arg2, frame)
                if type1 == 'bool':
                    frame.set_var(act_instruction.arg1, 'bool', 'true' if data1 == 'false' else 'false')
                else :
                    exit(ExitCodes.runErrorBadType)
            #20
            elif act_instruction.type == 'INT2CHAR':
                type1, data1 = act_instruction.get_data_arg_type(act_instruction.arg2, frame)
                if type1 != 'int':
                    exit(ExitCodes.runErrorBadType)
                else:
                    try:
                        char = chr(int(data1))
                    except ValueError:
                        exit(ExitCodes.runErrorBadStringOperation)
                    frame.set_var(act_instruction.arg1, 'string', char)
            #21
            elif act_instruction.type == 'STRI2INT':
                type1, data1 = act_instruction.get_data_arg_type(act_instruction.arg2, frame)
                type2, data2 = act_instruction.get_data_arg_type(act_instruction.arg3, frame)

                if type1 != 'string' or type2 != 'int':
                    exit(ExitCodes.runErrorBadType)
                else:
                    i = int(data2)
                    if i >= 0 and i <= len(data1) - 1:
                        ordd = ord(data1[i])
                        frame.set_var(act_instruction.arg1, 'int', ordd)
                    else:
                        exit(ExitCodes.runErrorBadStringOperation)
            #22
            elif act_instruction.type == 'READ' :
                type1, data1 = act_instruction.get_data_arg_type(act_instruction.arg2, frame)

                if len(self.getInputPath()) :
                    try :
                        with open(self.getInputPath()) as file :
                            uis = file.read().splitlines()
                    except FileNotFoundError :
                        exit(ExitCodes.inFileError)
                    
                    try:
                        userInput = uis[lineCounter]
                    except IndexError:
                        frame.set_var(act_instruction.arg1, 'nil', '')
                        continue
                    finally :
                        lineCounter += 1
                else :
                    try :
                        userInput = input()
                    except Exception :
                        exit(ExitCodes.inFileError)
                
                if data1 == 'int' :
                    try:
                        number = str(int(userInput))
                    except :
                        frame.set_var(act_instruction.arg1, 'nil', '')
                    else :
                        frame.set_var(act_instruction.arg1, 'int', number)
                elif data1 == 'bool' :
                    if userInput.lower() == 'true' :
                        frame.set_var(act_instruction.arg1, 'bool', 'true')
                    elif userInput.lower() == 'false' :
                        frame.set_var(act_instruction.arg1, 'bool', 'false')
                    else :
                        frame.set_var(act_instruction.arg1, 'bool', 'false')
                else :
                    frame.set_var(act_instruction.arg1, 'string', userInput)
            #23
            elif act_instruction.type == 'WRITE':
                aType, aData = act_instruction.get_data_arg_type(act_instruction.arg1, frame)

                if aData == None:
                    exit(ExitCodes.runErrorMissingValue)

                else:
                    if (aData == 'nil') and (aType == 'nil'):
                        aData = ''
                    print(aData, end='')
            #24
            elif act_instruction.type == 'CONCAT':
                type1, data1 = act_instruction.get_data_arg_type(act_instruction.arg2, frame)
                type2, data2 = act_instruction.get_data_arg_type(act_instruction.arg3, frame)

                if type1 != 'string' or type2 != 'string':
                    exit(ExitCodes.runErrorBadType)
                else:
                    if data1 is None:
                        data1 = ''
                    else:
                        data1
                    if data2 is None:
                        data2 = ''
                    else:
                        data2

                    frame.set_var(act_instruction.arg1, 'string', data1 + data2)
            #25
            elif act_instruction.type == 'STRLEN':
                type1, data1 = act_instruction.get_data_arg_type(act_instruction.arg2, frame)

                if type1 != 'string':
                    exit(ExitCodes.runErrorBadType)
                else:
                    frame.set_var(act_instruction.arg1, 'int', len(data1))
            #26
            elif act_instruction.type == 'GETCHAR' :
                type1, data1 = act_instruction.get_data_arg_type(act_instruction.arg2, frame)
                type2, data2 = act_instruction.get_data_arg_type(act_instruction.arg3, frame)

                if type1 != 'string' or type2 != 'int' :
                    exit(ExitCodes.runErrorBadType)
                else :      
                    if int(data2) < 0 or int(data2) >= len(data1) :
                        exit(ExitCodes.runErrorBadStringOperation)
                    else :
                        frame.set_var(act_instruction.arg1, 'string', data1[int(data2)])
            #27
            elif act_instruction.type == 'SETCHAR':
                type1, data1 = act_instruction.get_data_arg_type(act_instruction.arg2, frame)
                type2, data2 = act_instruction.get_data_arg_type(act_instruction.arg3, frame)
                typeV, dataV = act_instruction.get_data_arg_type(act_instruction.arg1, frame)

                if type1 != 'int' or type2 != 'string' or typeV != 'string':
                    exit(ExitCodes.runErrorBadType)
                else:
                    if int(data1) < 0 or int(data1) >= len(dataV) or dataV == '':
                        exit(ExitCodes.runErrorBadStringOperation)
                    
                    if data2 != '':
                        data_list = list(dataV)
                        data_list[int(data1)] = data2[0]
                        dataV = "".join(data_list)
                        frame.set_var(act_instruction.arg1, 'string', dataV)
                    else:
                        exit(ExitCodes.runErrorBadStringOperation)
            #28
            elif act_instruction.type == 'TYPE':
                type1 = act_instruction.get_type(act_instruction.arg2, frame)
                if type1 is None:
                    type1 = ''
                frame.set_var(act_instruction.arg1, 'string', type1)
            #29
            elif act_instruction.type == 'LABEL':
                continue
            #30
            elif act_instruction.type == 'JUMP':
                instructionList.jump(act_instruction.arg1)
            #31
            elif act_instruction.type == 'JUMPIFEQ':
                type1, data1 = act_instruction.get_data_arg_type(act_instruction.arg2, frame)
                type2, data2 = act_instruction.get_data_arg_type(act_instruction.arg3, frame)
                instructionList.label_checking(act_instruction.arg1)

                if (type1 == 'nil') or (type2 == 'nil') or (type1 == type2):
                    if data1 == data2:
                        instructionList.jump(act_instruction.arg1)
                    else:
                        pass
                else:
                    exit(ExitCodes.runErrorBadType)
            #32
            elif act_instruction.type == 'JUMPIFNEQ':
                type1, data1 = act_instruction.get_data_arg_type(act_instruction.arg2, frame)
                type2, data2 = act_instruction.get_data_arg_type(act_instruction.arg3, frame)
                instructionList.label_checking(act_instruction.arg1)

                if (type1 == 'nil') or (type2 == 'nil') or (type1 == type2):
                    if data1 != data2:
                        instructionList.jump(act_instruction.arg1)
                    else:
                        pass
                else:
                    exit(ExitCodes.runErrorBadType)
            #33
            elif act_instruction.type == 'EXIT':
                type1, data1 = act_instruction.get_data_arg_type(act_instruction.arg1, frame)

                if (type1 == 'int'):
                    if int(data1) < 0 or int(data1) > 49:
                        exit(ExitCodes.runErrorZeroDivision)
                    else:
                        exit(int(data1))
                else:
                    exit(ExitCodes.runErrorBadType)
            #34        
            elif act_instruction.type == 'DPRINT':
                aType, aData = act_instruction.get_data_arg_type(act_instruction.arg1, frame)

                if aData == None:
                    exit(ExitCodes.runErrorMissingValue)

                else:
                    if (aData == 'nil') and (aType == 'nil'):
                        aData = ''
                    sys.stderr.write(aData)
            #35
            elif act_instruction.type == 'BREAK':
                pass


                    
                



