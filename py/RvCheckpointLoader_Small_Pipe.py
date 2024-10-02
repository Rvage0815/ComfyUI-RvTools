import comfy
import comfy.sd
import torch
import folder_paths

from ..core import CATEGORY

MAX_RESOLUTION = 32768

class RCheckpointLoader_Small_Pipe:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Checkpoint": (folder_paths.get_filename_list("checkpoints"),),
                "Vae": (["Baked VAE"] + folder_paths.get_filename_list("vae"),),
                "Baked_Clip": ("BOOLEAN", {"default": True},),
                "Use_Clip_Layer": ("BOOLEAN", {"default": True},),
                "stop_at_clip_layer": ("INT", {"default": -1, "min": -24, "max": -1, "step": 1},),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 4096}),
            },
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.SETTINGS.value

    RETURN_TYPES = ("pipe",)
    FUNCTION = "execute"

    def execute(self, Checkpoint, Vae, Baked_Clip, Use_Clip_Layer, stop_at_clip_layer, batch_size):
        ckpt_path = folder_paths.get_full_path("checkpoints", Checkpoint)
        output_vae = False

        if Vae == "Baked VAE": output_vae = True

        ckpt = comfy.sd.load_checkpoint_guess_config(ckpt_path, output_vae=output_vae, output_clip=Baked_Clip, embedding_directory=folder_paths.get_folder_paths("embeddings"),)

        vae_path = ""

        if Vae == "Baked VAE":
            vae = ckpt[:3][2]
        else:
            vae_path = folder_paths.get_full_path("vae", Vae)
            vae = comfy.sd.VAE(sd=comfy.utils.load_torch_file(vae_path))

        if Baked_Clip:
            clip = ckpt[:3][1].clone()
            if Use_Clip_Layer: clip.clip_layer(stop_at_clip_layer)
        else:
            clip = None

        #model, clip, vae, batch_size, modelname, vae_name = pipe

        rlist = []
        rlist.append(ckpt[:3][0])
        rlist.append(clip)
        rlist.append(vae)
        rlist.append(int(batch_size))     #batch_size
        rlist.append(str(Checkpoint))     #str(ckpt_path)) #model_name
        rlist.append(str(vae_path))       #vae_name

        return (rlist,)

NODE_NAME = 'Checkpoint Loader (Small Pipe) // RvTools'
NODE_DESC = 'Checkpoint Loader (Small Pipe)'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RCheckpointLoader_Small_Pipe
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}
