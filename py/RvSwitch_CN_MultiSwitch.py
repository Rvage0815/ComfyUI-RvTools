from ..core import CATEGORY

class RvSwitch_CN_MultiSwitch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
            },
            "optional": {
                "input1": ("CONTROL_NET",),
                "input2": ("CONTROL_NET",),
                "input3": ("CONTROL_NET",),
                "input4": ("CONTROL_NET",),
                "input5": ("CONTROL_NET",),
            }
        }

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.MULTISWITCHES.value
    RETURN_TYPES = ("CONTROL_NET",)
    RETURN_NAMES = ("cn",)

    FUNCTION = "execute"

    def execute(self, input1=None, input2=None, input3=None, input4=None, input5=None):
        

        if input1 != None:
            return (input1,)
        elif input2 != None:
            return (input2,)
        elif input3 != None:
            return (input3,)
        elif input4 != None:
            return (input4,)
        elif input5 != None:
            return (input5,)
        else:
            raise ValueError("Missing Input: Multi ControlNet Switch has no active Input")

NODE_NAME = 'ControlNet Multi-Switch // RvTools'
NODE_DESC = 'ControlNet Multi-Switch'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvSwitch_CN_MultiSwitch
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}
