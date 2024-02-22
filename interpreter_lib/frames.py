#author: Marcel Feiler
#project: IPP - 2 (ippcode23)
#FIT VUT BR

from interpreter_lib.exit_codes import *
import interpreter_lib.instructions as i

class Frames:
    def __init__(self):
        super().__init__()
        self.globalFrame = {}
        self.__frameStack = []
        self.__tmpFrame = {}
        self.istmpFrame = False
    
    def get_temp_frame(self):
        if self.istmpFrame:
            return self.__tmpFrame
        else:
            return None
    
    def get_local_frame(self):
        if len(self.__frameStack) > 0:
            return self.__frameStack[-1]
        else:
            return None
        

    def get_global_frame(self):
        return self.globalFrame

    def create_frame(self):
        self.istmpFrame = True
        self.__tmpFrame = {}   

    def push_frame(self):
        if self.istmpFrame == False:
            exit(ExitCodes.runErrorMissingFrame)
        else:
            self.__frameStack.append(self.__tmpFrame)
            self.istmpFrame = False
    
    def pop_frame(self):
        if not(len(self.__frameStack)):
            exit(ExitCodes.runErrorMissingFrame)
        else:
            self.__tmpFrame = self.__frameStack.pop()
            self.istmpFrame = True

    def set_var(self, argument, typy, data) :
        frame, name = i.Instruction.var_split(argument)
        
        if frame == 'GF':
            frame_object = self.get_global_frame()
        elif frame == 'LF':
            frame_object = self.get_local_frame()
        elif frame == 'TF':
            frame_object = self.get_temp_frame()
        else:
            frame_object = None

        if frame_object is None :
            exit(ExitCodes.runErrorMissingFrame)
        if name not in frame_object :
            exit(ExitCodes.runErrorMissingVar)
        frame_object[name]['type'] = typy
        frame_object[name]['data'] = data

    def def_var(self, argument) :
        frame, name = i.Instruction.var_split(argument)

        if frame == 'GF':
            frame_object = self.get_global_frame()
        elif frame == 'LF':
            frame_object = self.get_local_frame()
        elif frame == 'TF':
            frame_object = self.get_temp_frame()
        else:
            frame_object = None
        
        if frame_object is None :
            exit(ExitCodes.runErrorMissingFrame)
        else :
            if name in frame_object :
                exit(ExitCodes.semanticError)
            else :
                frame_object[name] = {'data': None, 'type': None}

