#from .anytype import *

from ..core import CATEGORY

class RvPipe_InputSettings_VHS_Out:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"pipe": ("pipe",),}}

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.PIPE.value
    RETURN_TYPES = ("pipe", "INT", "INT", "INT", "INT", "INT", "INT", ["center","top", "bottom", "left", "right"], ["lanczos", "nearest", "bilinear", "bicubic", "area", "nearest-exact"], "FLOAT",)
    RETURN_NAMES = ("pipe", "load_cap", "skip_first_frames", "select_every_nth", "overlap", "images_in_preview", "images_in_filter_previews", "preview_crop_pos", "preview_crop_interpol", "frame_rate",)

    FUNCTION = "execute"

    def execute(self, pipe=None, ):
        load_cap, skip_first_frames, select_every_nth, overlap, images_in_preview, images_in_filter_previews, preview_crop_pos, preview_crop_interpol, frame_rate  = pipe
        
        return pipe, load_cap, skip_first_frames, select_every_nth, overlap, images_in_preview, images_in_filter_previews, preview_crop_pos, preview_crop_interpol, frame_rate

NODE_NAME = 'Input Settings Out (VHS) // RvTools'
NODE_DESC = 'Input Settings Out (VHS)'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvPipe_InputSettings_VHS_Out
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}
