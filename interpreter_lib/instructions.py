#author: Marcel Feiler
#project: IPP - 2 (ippcode23)
#FIT VUT BR

from interpreter_lib.exit_codes import *
from interpreter_lib.frames import Frames


############################################################



####################

class Instruction():
    def __init__(self, type, arg1 = None, arg2 = None, arg3 = None):
        super().__init__()
        self.type = type
        self.argsCount = 0

        if arg1 is not None:
            self.arg1 = {'type': arg1.attrib['type'], 'data': (arg1.text if arg1.text is not None else '')}
            self.argsCount += 1

        if arg2 is not None:
            self.arg2 = {'type': arg2.attrib['type'], 'data': (arg2.text if arg2.text is not None else '')}
            self.argsCount += 1

        if arg3 is not None:
            self.arg3 = {'type': arg3.attrib['type'], 'data': (arg3.text if arg3.text is not None else '')}
            self.argsCount += 1

    #help function for set_var, def_var
    @staticmethod
    def var_split(var):
        return var['data'].split('@', 1)
   
    #help function for TYPE instruction (core)
    def get_type(self, argument, frames):
        possible_types = ['int', 'bool', 'string', 'type', 'label', 'nil']
        if argument['type'] not in possible_types:
            frame, data = self.var_split(argument)
            
            if frame == 'GF':
                frame_object = frames.get_global_frame()
            elif frame == 'LF':
                frame_object = frames.get_local_frame()
            elif frame == 'TF':
                frame_object = frames.get_temp_frame()
            else:
                frame_object = None

            if frame_object is None:
                exit(ExitCodes.runErrorMissingFrame)

            if data in frame_object:
                if frame_object[data]['type'] is None:
                    return None
                else:
                    return frame_object[data]['type']
            else:
                exit(ExitCodes.runErrorMissingVar) 

        else:
            return argument['type']
        

    def get_data_arg_type(self, argument, frameClassObj):
        possible_types = ['int', 'bool', 'string', 'type', 'label', 'nil']
        if argument['type'] not in possible_types:
            frame, data = self.var_split(argument)

            if frame == 'GF':
                frame_object = frameClassObj.get_global_frame()
            elif frame == 'LF':
                frame_object = frameClassObj.get_local_frame()
            elif frame == 'TF':
                frame_object = frameClassObj.get_temp_frame()
            else:
                frame_object = None


            if frame_object is None:
                exit(ExitCodes.runErrorMissingFrame)

            if data in frame_object:
                if (frame_object[data]['type'] is None) or (frame_object[data]['data'] is None):
                    exit(ExitCodes.runErrorMissingValue)
                else:
                    return(frame_object[data]['type'], frame_object[data]['data'])
            else:
                exit(ExitCodes.runErrorMissingVar)

        else:
            return(argument['type'], argument['data'])
                

        




#######################################################################
    #content is operand's data and executing code
   