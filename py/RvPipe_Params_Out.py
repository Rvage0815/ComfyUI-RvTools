#from .anytype import *

from ..core import CATEGORY

class RvPipe_Params_Out:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"pipe": ("pipe",),}}

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.PIPE.value
    RETURN_TYPES = ("pipe", "INT", "FLOAT", "STRING", "STRING", "STRING", "STRING", "STRING", "INT", "INT", "INT", "STRING",)
    RETURN_NAMES = ("pipe", "steps", "cfg", "sampler_name", "scheduler", "positive", "negative", "modelname", "width", "height", "seed_value", "loras",)

    FUNCTION = "execute"

    def execute(self, pipe=None, ):
        steps, cfg, sampler_name, scheduler, positive, negative, modelname, width, height, seed_value, loras = pipe
        return pipe, steps, cfg, sampler_name, scheduler, positive, negative, modelname, width, height, seed_value, loras

NODE_NAME = 'Params Out/Edit // RvTools'
NODE_DESC = 'Params Out'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvPipe_Params_Out
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}
