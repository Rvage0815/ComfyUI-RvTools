import comfy
import comfy.sd
import torch
import folder_paths

from ..core import CATEGORY

MAX_RESOLUTION = 32768

class RCheckpointLoader_Pipe:
    resolution =     ["Custom",
                      "512x512 (1:1)",              
                      "512x682 (3:4)",
                      "512x768 (2:3)",
                      "512x910 (9:16)",
                      "512x952 (1:1.85)",
                      "512x1024 (1:2)",
                      "512x1224 (1:2.39)",
                      "682x512 (4:3)",
                      "768x512 (3:2)",
                      "910x512 (16:9)",
                      "952x512 (1.85:1)",
                      "1024x512 (2:1)",
                      "1224x512 (2.39:1)",
                      "640x1536 (9:21)",
                      "768x1344 (9:16)",
                      "832x1216 (2:3)",
                      "896x1152 (3:4)",
                      "1024x1024 (1:1)",
                      "1152x896 (4:3)",
                      "1216x832 (3:2)",
                      "1344x768 (16:9)",
                      "1536x640 (21:9)" 
                      ]

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
                "resolution": (s.resolution,),
                "width": ("INT", {"default": 512, "min": 16, "max": MAX_RESOLUTION, "step": 8},),
                "height": ("INT", {"default": 512, "min": 16, "max": MAX_RESOLUTION, "step": 8},),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 4096}),
            },
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.SETTINGS.value

    RETURN_TYPES = ("pipe",)
    FUNCTION = "execute"

    def execute(self, Checkpoint, Vae, Baked_Clip, Use_Clip_Layer, stop_at_clip_layer, batch_size, resolution, width, height):
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

        #if(resolution == "Custom"):
            #width, height = 512, 512
        if(resolution == "512x512 (1:1)"):
            width, height = 512, 512
        if(resolution == "512x682 (3:4)"):
            width, height = 512, 682
        if(resolution == "512x768 (2:3)"):
            width, height = 512, 768
        if(resolution == "512x910 (9:16)"):
            width, height = 512, 910
        if(resolution == "512x952 (1:1.85)"):
            width, height = 512, 952
        if(resolution == "512x1024 (1:2)"):
            width, height = 512, 1024
        if(resolution == "512x1224 (1:2.39)"):
            width, height = 512, 1224
        if(resolution == "682x512 (4:3)"):
            width, height = 682, 512
        if(resolution == "768x512 (3:2)"):
            width, height = 768, 512
        if(resolution == "910x512 (16:9)"):
            width, height = 910, 512
        if(resolution == "952x512 (1.85:1)"):
            width, height = 952, 512
        if(resolution == "1024x512 (2:1)"):
            width, height = 1024, 512
        if(resolution == "1224x512 (2.39:1)"):
            width, height = 1224, 512
        #sdxl
        if(resolution == "640x1536 (9:21)"):
            width, height = 640, 1536
        if(resolution == "768x1344 (9:16)"):
            width, height = 768, 1344
        if(resolution == "832x1216 (2:3)"):
            width, height = 832, 1216
        if(resolution == "896x1152 (3:4)"):
            width, height = 896, 1152
        if(resolution == "1024x1024 (1:1)"):
            width, height = 1024, 1024
        if(resolution == "1152x896 (4:3)"):
            width, height = 1152, 896
        if(resolution == "1216x832 (3:2)"):
            width, height = 1216, 832
        if(resolution == "1344x768 (16:9)"):
            width, height = 1344, 768
        if(resolution == "1536x640 (21:9)"):
            width, height = 1536, 640

        latent = torch.zeros([batch_size, 4, height // 8, width // 8])

        #model, clip, vae, latent, width, height, batch_size, modelname, vae_name = pipe

        rlist = []
        rlist.append(ckpt[:3][0])
        rlist.append(clip)
        rlist.append(vae)
        rlist.append({"samples": latent}) #latents
        rlist.append(int(width))
        rlist.append(int(height))
        rlist.append(int(batch_size))
        rlist.append(str(Checkpoint))   #str(ckpt_path)) #model_name
        rlist.append(str(vae_path))  #vae_name

        return (rlist,)

NODE_NAME = 'Checkpoint Loader II (Pipe) // RvTools'
NODE_DESC = 'Checkpoint Loader II (Pipe)'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RCheckpointLoader_Pipe
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}
