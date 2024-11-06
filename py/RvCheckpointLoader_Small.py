import comfy
import comfy.sd
import torch
import folder_paths

from ..core import CATEGORY

MAX_RESOLUTION = 32768

class RCheckpointLoaderSmall:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Checkpoint": (folder_paths.get_filename_list("checkpoints"),),
                "Vae": (["Baked VAE"] + folder_paths.get_filename_list("vae"),),
                "stop_at_clip_layer": ("INT", {"default": -1, "min": -24, "max": -1, "step": 1},),
            },
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.CHECKPOINT.value

    RETURN_TYPES = ("MODEL", "VAE", "CLIP",)
    RETURN_NAMES = ("model", "vae", "clip",)
    FUNCTION = "execute"

    def execute(self, Checkpoint, Vae, stop_at_clip_layer):
        ckpt_path = folder_paths.get_full_path("checkpoints", Checkpoint)
        output_vae = False

        if Vae == "Baked VAE": output_vae = True

        ckpt = comfy.sd.load_checkpoint_guess_config(ckpt_path, output_vae=output_vae, output_clip=True, embedding_directory=folder_paths.get_folder_paths("embeddings"),)

        vae_path = ""

        if Vae == "Baked VAE":
            vae = ckpt[:3][2]
        else:
            vae_path = folder_paths.get_full_path("vae", Vae)
            vae = comfy.sd.VAE(sd=comfy.utils.load_torch_file(vae_path))

        clip = ckpt[:3][1].clone()
        clip.clip_layer(stop_at_clip_layer)

        return (ckpt[:3][0], vae, clip,)

NODE_NAME = 'Checkpoint Loader (Small) // RvTools'
NODE_DESC = 'Checkpoint Loader Small'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RCheckpointLoaderSmall
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}
