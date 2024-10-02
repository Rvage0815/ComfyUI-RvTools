#from .anytype import *

from ..core import CATEGORY

class RvPipe_Checkpoint_Loader_Small_OUT:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"pipe": ("pipe",),}}

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.PIPE.value
    RETURN_TYPES = ("pipe", "MODEL", "CLIP", "VAE", "INT",        "STRING",     "STRING",)
    RETURN_NAMES = ("pipe", "model", "clip", "vae", "batch_size", "model_name", "vae_name",)

    FUNCTION = "execute"

    def execute(self, pipe=None, ):
        model, clip, vae, batch_size, modelname, vae_name = pipe
        
        return pipe, model, clip, vae, batch_size, modelname, vae_name

NODE_NAME = 'Checkpoint Loader Small Pipe-Out // RvTools'
NODE_DESC = 'Checkpoint Loader Small Pipe-Out'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvPipe_Checkpoint_Loader_Small_OUT
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}
