#from .anytype import *

from ..core import CATEGORY

class RvPipe_Checkpoint_Loader_Small_IN:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "pipe": ("pipe",),
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "vae": ("VAE",),
                "batch_size": ("INT",{"forceInput": True}),
                "modelname": ("STRING",{"forceInput": True}),
                "vae_name": ("STRING",{"forceInput": True}),
            }
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.CHECKPOINT.value
    RETURN_TYPES = ("pipe",)

    FUNCTION = "execute"

    def execute(self, pipe=None, model=None, clip=None, vae=None, batch_size=None, modelname=None, vae_name=None):
        model_original = None
        clip_original = None
        vae_original = None
        batch_size_original = None
        modelname_original = None
        vae_name_original = None

        if pipe != None:
            model_original, clip_original, vae_original, batch_size_original, modelname_original, vae_name_original = pipe

        RBusAnyMod = []

        RBusAnyMod.append(model if model is not None else model_original)
        RBusAnyMod.append(clip if clip is not None else clip_original)
        RBusAnyMod.append(vae if vae is not None else vae_original)
        RBusAnyMod.append(batch_size if batch_size is not None else batch_size_original)
        RBusAnyMod.append(modelname if modelname is not None else modelname_original)
        RBusAnyMod.append(vae_name if vae_name is not None else vae_name_original)

        return (RBusAnyMod,)

NODE_NAME = 'Checkpoint Loader Small Pipe-In // RvTools'
NODE_DESC = 'Pipe Out (Checkpoint Loader Small + v3)'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvPipe_Checkpoint_Loader_Small_IN
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}
