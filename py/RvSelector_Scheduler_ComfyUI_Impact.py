
import comfy

from ..core import CATEGORY

SCHEDULERS_COMFY = comfy.samplers.KSampler.SCHEDULERS
SCHEDULERS_IMPACT = comfy.samplers.KSampler.SCHEDULERS + ['AYS SDXL', 'AYS SD1', 'AYS SVD', 'GITS[coeff=1.2]']

class RvSelector_Scheduler_ComfyUI_Impact:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "scheduler_comfy": (SCHEDULERS_COMFY,),
                "scheduler_impact": (SCHEDULERS_IMPACT,),
                }
            }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.SELECTOR.value
    RETURN_TYPES = (
        SCHEDULERS_COMFY,
        SCHEDULERS_IMPACT,)
    RETURN_NAMES = ("comfy", "impact",)

    FUNCTION = "execute"

    def execute(self, scheduler_comfy, scheduler_impact):
        return (scheduler_comfy, scheduler_impact,)

NODE_NAME = 'Scheduler Selector (ComfyUI/Impact) // RvTools'
NODE_DESC = 'Scheduler Selector (ComfyUI/Impact)'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvSelector_Scheduler_ComfyUI_Impact
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}
