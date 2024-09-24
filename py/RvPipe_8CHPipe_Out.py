from .anytype import *

from ..core import CATEGORY

class RvPipe_8CHPipe_Out:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"pipe": ("pipe",),}}

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.PIPE.value
    RETURN_TYPES = ("pipe", any, any, any, any, any, any, any, any,)
    RETURN_NAMES = ("pipe", "any_1", "any_2", "any_3", "any_4", "any_5", "any_6", "any_7", "any_8",)

    FUNCTION = "execute"

    def execute(self, pipe=None,):
        any_1, any_2, any_3, any_4, any_5, any_6, any_7, any_8 = pipe
        return pipe, any_1, any_2, any_3, any_4, any_5, any_6, any_7, any_8

NODE_NAME = '8CH Bus Out // RvTools'
NODE_DESC = '8CH Pipe Out'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvPipe_8CHPipe_Out
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}
