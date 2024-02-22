#author: Marcel Feiler
#project: IPP - 2 (ippcode23)
#FIT VUT BR

import interpreter_lib.instructions as instruction
from interpreter_lib.exit_codes import *

class InstructionList() :
    def __init__(self):
        super().__init__()
        self.instructionCounter = 0
        self.list = {}
        self.current = 1
        self.labels = {}
        self.callstack = []
    
    #inserting a new instruction
    def instruction_insert(self, instruction: instruction.Instruction):
        self.instructionCounter += 1
        self.list[self.instructionCounter] = instruction
        if instruction.type == 'LABEL':
            name = instruction.arg1['data']
            if name not in self.labels :
                self.labels[name] = self.instructionCounter
            else :
                exit(ExitCodes.semanticError)

    #receiving another instruction    
    def next_instruction(self):
        if (self.current <= self.instructionCounter) :
            self.current += 1
            return self.list[self.current - 1]
        else:
            return None

    def position_store(self) :
        self.callstack.append(self.current)

    def position_restore(self) :
        if len(self.callstack) :
            self.current = self.callstack.pop()
        else :
            exit(ExitCodes.runErrorMissingValue)

    def jump(self, argument) :
        name = argument['data']
        if name in self.labels :
            self.current = self.labels[name]
        else :
            exit(ExitCodes.semanticError)

    #help function for jumpifeq jumpifneq
    def label_checking(self, argument) :
        name = argument['data']
        if name not in self.labels :
            exit(ExitCodes.semanticError)

    #help function for string checking
    def string_fixation(self, string):
        index: int = string.find('\\')
        while(index != -1) :
            string = string.replace(string[index:index+4], chr(int(string[index+1:index+4])))
            index = string.find('\\', index + 1)
        return string
        
    #final string checking   
    def string_checking(self) :
        for ins in self.list:
            instruction = self.list[ins]
            if hasattr(instruction, 'arg1') :
                if instruction.arg1['type'] == 'string' :
                    instruction.arg1['data'] = self.string_fixation(instruction.arg1['data'])
            if hasattr(instruction, 'arg2') :
                if instruction.arg2['type'] == 'string' :
                    instruction.arg2['data'] = self.string_fixation(instruction.arg2['data'])
            if hasattr(instruction, 'arg3') :
                if instruction.arg3['type'] == 'string' :
                    instruction.arg3['data'] = self.string_fixation(instruction.arg3['data'])

