from .anytype import *

from ..core import CATEGORY

class RvPipe_SamplerSettings_Small_Out:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"pipe": ("pipe",),}}

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.PIPE.value
    RETURN_TYPES = ("pipe",  any,       any,        "INT",   "FLOAT")
    RETURN_NAMES = ("pipe", "sampler", "scheduler", "steps", "cfg")

    FUNCTION = "execute"

    def execute(self, pipe=None, ):
        sampler, scheduler, steps, cfg  = pipe
        
        return pipe, sampler, scheduler, steps, cfg

NODE_NAME = 'Sampler Settings Out (Small) // RvTools'
NODE_DESC = 'Sampler Settings Out (Small)'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvPipe_SamplerSettings_Small_Out
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}
