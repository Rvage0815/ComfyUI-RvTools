import comfy
import comfy.sd
import torch
import folder_paths

from ..core import CATEGORY

MAX_RESOLUTION = 32768
CLIP_MODELS = folder_paths.get_filename_list("clip") + ["None"]
DIFF_MODELS = folder_paths.get_filename_list("diffusion_models") + ["None"]
CKPT_MODELS = folder_paths.get_filename_list("checkpoints") + ["None"]

class RCheckpointLoader_v3_Pipe:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "ckpt_name": (CKPT_MODELS, {"default": "None"},),
                "unet_name": (DIFF_MODELS, {"default": "None"},), 
                "weight_dtype": (["default", "fp8_e4m3fn", "fp8_e4m3fn_fast", "fp8_e5m2"],),
                "clip_name1": (CLIP_MODELS, {"default": "None"},),
                "clip_name2": (CLIP_MODELS, {"default": "None"},),
                "clip_name3": (CLIP_MODELS, {"default": "None"},),
                "clip_type_": (["sdxl", "sd3", "flux"], {"default": "flux"},),
                "vae": (["Baked VAE"] + folder_paths.get_filename_list("vae"),),
                "baked_clip": ("BOOLEAN", {"default": True},),
                "enable_clip_layer": ("BOOLEAN", {"default": True},),
                "stop_at_clip_layer": ("INT", {"default": -1, "min": -24, "max": -1, "step": 1},),
                "load_unet_checkpoint": ("BOOLEAN", {"default": False},),
            },
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.CHECKPOINT.value

    RETURN_TYPES = ("pipe",)
    FUNCTION = "execute"

    def execute(self, ckpt_name, unet_name, weight_dtype, clip_name1, clip_name2, clip_name3, clip_type_, vae, load_unet_checkpoint, baked_clip, enable_clip_layer, stop_at_clip_layer):
        checkpoint = ""
        vae_path = ""
        clip_path1 = ""
        clip_path2 = ""
        clip_path3 = ""
        
        baked_vae = False
        clip = None

        if vae == "Baked VAE": baked_vae = True 

        if ckpt_name in (None, 'undefined', 'None') and unet_name in (None, 'undefined', 'None'):   #no checkpoint selected
            raise ValueError("Missing Input: No Checkpoint selected")
        
        elif ckpt_name not in (None, 'undefined', 'None') and load_unet_checkpoint == False:
             ckpt_path = folder_paths.get_full_path("checkpoints", ckpt_name)
             #load the checkpoint
             ckpt = comfy.sd.load_checkpoint_guess_config(ckpt_path, output_vae=baked_vae, output_clip=baked_clip, embedding_directory=folder_paths.get_folder_paths("embeddings"),)
             checkpoint = ckpt_name #pass the name without path

             #load the clip
             if baked_clip:
                clip = ckpt[:3][1].clone()
                if enable_clip_layer: clip.clip_layer(stop_at_clip_layer)

        elif unet_name not in (None, 'undefined', 'None') and load_unet_checkpoint:
             model_options = {}
             if weight_dtype == "fp8_e4m3fn":
                 model_options["dtype"] = torch.float8_e4m3fn
             elif weight_dtype == "fp8_e4m3fn_fast":
                 model_options["dtype"] = torch.float8_e4m3fn
                 model_options["fp8_optimizations"] = True
             elif weight_dtype == "fp8_e5m2":
                 model_options["dtype"] = torch.float8_e5m2

             ckpt_path = folder_paths.get_full_path_or_raise("diffusion_models", unet_name) #unet
             #load the checkpoint
             ckpt = comfy.sd.load_diffusion_model(ckpt_path, model_options=model_options) 
             checkpoint = unet_name #pass the name without path

        else:
            raise ValueError("Missing Input: No Checkpoint selected or wrong combination of settings. to load a regular checkpoint 'ckpt_name' select one AND set 'load_unet_checkpoint' = False. to load a unet checkpoint 'unet_name' select one AND set 'load_unet_checkpoint'= True") #no checkpoint selected

        #load the VAE
        if vae == "Baked VAE":
            if load_unet_checkpoint == False:
                loaded_vae = ckpt[:3][2]
            else: raise ValueError("Missing Input: Select a VAE File")
        else:
            vae_path = folder_paths.get_full_path("vae", vae)
            loaded_vae = comfy.sd.VAE(sd=comfy.utils.load_torch_file(vae_path))

        #load the clip
        if clip_type_ == "sdxl":
            clip_type = comfy.sd.CLIPType.STABLE_DIFFUSION
        elif clip_type_ == "sd3":
            clip_type = comfy.sd.CLIPType.SD3
        elif clip_type_ == "flux":
            clip_type = comfy.sd.CLIPType.FLUX

             
        if not baked_clip:
            if clip_name1 not in (None, 'undefined', 'None'):
                clip_path1 = folder_paths.get_full_path_or_raise("clip", clip_name1)
            else:
               raise ValueError("Missing Input: Select a Clip Model for 'clip_name1' or set 'baked_clip' = True")

            if clip_name2 not in (None, 'undefined', 'None'):
                clip_path2 = folder_paths.get_full_path_or_raise("clip", clip_name2)
            else:
               raise ValueError("Missing Input: Select a Clip Model for 'clip_name2'")

            if clip_name3 not in (None, 'undefined', 'None'):
               clip_path3 = folder_paths.get_full_path_or_raise("clip", clip_name3)
             
            if not clip_path1 == "" and not clip_path2 == "" and not clip_path3 == "": 
               clip = comfy.sd.load_clip(ckpt_paths=[clip_path1, clip_path2, clip_path3], embedding_directory=folder_paths.get_folder_paths("embeddings"), clip_type=clip_type)
            elif not clip_path1 == "" and not clip_path2 == "": 
               clip = comfy.sd.load_clip(ckpt_paths=[clip_path1, clip_path2], embedding_directory=folder_paths.get_folder_paths("embeddings"), clip_type=clip_type)
            elif not clip_path1 == "": 
               clip = comfy.sd.load_clip(ckpt_paths=[clip_path1], embedding_directory=folder_paths.get_folder_paths("embeddings"), clip_type=clip_type)
        else:
            if load_unet_checkpoint: raise ValueError("Missing Input: CLIP, set 'baked_clip' to false and select clip models.")
        
        if clip == None:
            raise ValueError("Missing Input: CLIP")
        
        #model, clip, vae, modelname, vae_name = pipe

        rlist = []
        
        if load_unet_checkpoint: rlist.append(ckpt)
        else: rlist.append(ckpt[:3][0])

        rlist.append(clip)
        rlist.append(loaded_vae)
        rlist.append(int(1))               #batch_size (unused, just here to use the existing small pipe in/out node)
        rlist.append(checkpoint)           #model_name without path

        if vae == "Baked VAE":
           rlist.append('')                #empty string no file selected
        else:
            rlist.append(str(vae_path))    #vae_name

        return (rlist,)

NODE_NAME = 'Checkpoint Loader v3 (Pipe) // RvTools'
NODE_DESC = 'Checkpoint Loader v3 (Pipe)'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RCheckpointLoader_v3_Pipe
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}
