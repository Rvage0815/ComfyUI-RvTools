from .anytype import *

from ..core import CATEGORY

class RvPipe_SamplerSettings_DualScheduler_Out:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"pipe": ("pipe",),}}


    CATEGORY = CATEGORY.MAIN.value + CATEGORY.PIPE.value
    RETURN_TYPES = ("pipe", any, any, any, "INT", "FLOAT", "FLOAT", "UPSCALE_MODEL", "FLOAT")
    RETURN_NAMES = ("pipe", "sampler", "scheduler", "scheduler_2", "steps", "cfg", "flux_guidance", "upscale_model", "scale_by")

    FUNCTION = "execute"

    def execute(self, pipe=None, ):
        sampler, scheduler, scheduler_2, steps, cfg, flux_guidance, upscale_model, scale_by  = pipe
        
        return pipe, sampler, scheduler, scheduler_2, steps, cfg, flux_guidance, upscale_model, scale_by

NODE_NAME = 'Sampler Settings Out (Dual-Scheduler) // RvTools'
NODE_DESC = 'Sampler Settings Out (Dual-Scheduler)'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvPipe_SamplerSettings_DualScheduler_Out
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}
