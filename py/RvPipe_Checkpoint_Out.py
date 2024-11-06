#from .anytype import *

from ..core import CATEGORY

class RvPipe_Checkpoint_Out:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"pipe": ("pipe",),}}

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.CHECKPOINT.value
    RETURN_TYPES = ("pipe", "MODEL", "CLIP", "VAE", "LATENT", "INT",   "INT",    "INT",        "STRING",     "STRING",)
    RETURN_NAMES = ("pipe", "model", "clip", "vae", "latent", "width", "height", "batch_size", "model_name", "vae_name",)

    FUNCTION = "execute"

    def execute(self, pipe=None, ):
        model, clip, vae, latent, width, height, batch_size, modelname, vae_name = pipe
        
        return pipe, model, clip, vae, latent, width, height, batch_size, modelname, vae_name

NODE_NAME = 'Checkpoint Pipe-Out/Edit // RvTools'
NODE_DESC = 'Pipe Out (Checkpoint Loader v2)'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvPipe_Checkpoint_Out
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}
