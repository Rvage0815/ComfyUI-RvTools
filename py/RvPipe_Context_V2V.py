import comfy
import comfy.sd

from .anytype import *
from ..core import CATEGORY

SAMPLERS_COMFY = comfy.samplers.KSampler.SAMPLERS
SCHEDULERS_ANY = comfy.samplers.KSampler.SCHEDULERS + ['AYS SD1', 'AYS SDXL', 'AYS SVD', 'GITS[coeff=1.2]','simple_test']

#code is taken from rgthree context utils
_all_context_input_output_data = {
  "base_ctx": ("base_ctx", "pipe", "context"),
  "model": ("model", "MODEL", "model"),
  "clip": ("clip", "CLIP", "clip"),
  "vae": ("vae", "VAE", "vae"),
  "positive": ("positive", "CONDITIONING", "positive"),
  "negative": ("negative", "CONDITIONING", "negative"),
  "latent": ("latent", "LATENT", "latent"),
  "images": ("images", "IMAGE", "images"),
  "sampler": ("sampler", any, "sampler"),
  "scheduler": ("scheduler", any, "scheduler"),
  "audio": ("audio", "AUDIO", "audio"),
  "seed": ("seed", "INT", "seed"),
  "steps": ("steps", "INT", "steps"),
  "cfg": ("cfg", "FLOAT", "cfg"),
  "width": ("width", "INT", "width"),
  "height": ("height", "INT", "height"),
  "path": ("path", "STRING", "path"),
  "load_cap": ("load_cap", "INT", "load_cap"),
  "batch_size": ("batch_size", "INT", "batch_size"),
  "skip_first_frames": ("skip_first_frames", "INT", "skip_first_frames"),
  "select_every_nth": ("select_every_nth", "INT", "select_every_nth"),
  "overlap": ("overlap", "INT", "overlap"),
  "images_in_previews": ("images_in_previews", "INT", "images_in_previews"),
  "images_in_filter_previews": ("images_in_filter_previews", "INT", "images_in_filter_previews"),
  "preview_crop_pos": ("preview_crop_pos", ["center","top", "bottom", "left", "right"], "preview_crop_pos"),
  "preview_crop_interpol": ("preview_crop_interpol", ["lanczos", "nearest", "bilinear", "bicubic", "area", "nearest-exact"], "preview_crop_interpol"),
  "frame_rate": ("frame_rate", "FLOAT", "frame_rate"),
  "scale_by": ("scale_by", "FLOAT", "scale_by"),
  "images_per_batch": ("images_per_batch", "INT", "images_per_batch"),
 }

force_input_types = ["INT", "STRING", "FLOAT"]
force_input_names = ["sampler", "scheduler", "preview_crop_pos", "preview_crop_interpol"]

def _create_context_data(input_list=None):
  """Returns a tuple of context inputs, return types, and return names to use in a node"s def"""
  if input_list is None:
    input_list = _all_context_input_output_data.keys()
  list_ctx_return_types = []
  list_ctx_return_names = []
  ctx_optional_inputs = {}
  for inp in input_list:
    data = _all_context_input_output_data[inp]
    list_ctx_return_types.append(data[1])
    list_ctx_return_names.append(data[2])
    ctx_optional_inputs[data[0]] = tuple([data[1]] + ([{
      "forceInput": True
    }] if data[1] in force_input_types or data[0] in force_input_names else []))

  ctx_return_types = tuple(list_ctx_return_types)
  ctx_return_names = tuple(list_ctx_return_names)
  return (ctx_optional_inputs, ctx_return_types, ctx_return_names)


ALL_CTX_OPTIONAL_INPUTS, ALL_CTX_RETURN_TYPES, ALL_CTX_RETURN_NAMES = _create_context_data()

_original_ctx_inputs_list = [
  "base_ctx", "model", "clip", "vae", "positive", "negative", "latent", "images", "seed"
]
ORIG_CTX_OPTIONAL_INPUTS, ORIG_CTX_RETURN_TYPES, ORIG_CTX_RETURN_NAMES = _create_context_data(
  _original_ctx_inputs_list)


def new_context(base_ctx, **kwargs):
  """Creates a new context from the provided data, with an optional base ctx to start."""
  context = base_ctx if base_ctx is not None else None
  new_ctx = {}
  for key in _all_context_input_output_data:
    if key == "base_ctx":
      continue
    v = kwargs[key] if key in kwargs else None
    new_ctx[key] = v if v is not None else context[
      key] if context is not None and key in context else None
  return new_ctx


def merge_new_context(*args):
  """Creates a new context by merging provided contexts with the latter overriding same fields."""
  new_ctx = {}
  for key in _all_context_input_output_data:
    if key == "base_ctx":
      continue
    v = None
    # Move backwards through the passed contexts until we find a value and use it.
    for ctx in reversed(args):
      v = ctx[key] if not is_context_empty(ctx) and key in ctx else None
      if v is not None:
        break
    new_ctx[key] = v
  return new_ctx


def get_context_return_tuple(ctx, inputs_list=None):
  """Returns a tuple for returning in the order of the inputs list."""
  if inputs_list is None:
    inputs_list = _all_context_input_output_data.keys()
  tup_list = [
    ctx,
  ]
  for key in inputs_list:
    if key == "base_ctx":
      continue
    tup_list.append(ctx[key] if ctx is not None and key in ctx else None)
  return tuple(tup_list)


def get_orig_context_return_tuple(ctx):
  """Returns a tuple for returning from a node with only the original context keys."""
  return get_context_return_tuple(ctx, _original_ctx_inputs_list)


def is_context_empty(ctx):
  """Checks if the provided ctx is None or contains just None values."""
  return not ctx or all(v is None for v in ctx.values())

class RvPipe_Context_V2V:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
          "required": {},
          "optional": ALL_CTX_OPTIONAL_INPUTS,
          "hidden": {},
        }

    RETURN_TYPES = ALL_CTX_RETURN_TYPES
    RETURN_NAMES = ALL_CTX_RETURN_NAMES

    CATEGORY = CATEGORY.MAIN.value + CATEGORY.PIPE.value


    FUNCTION = "execute"

    def execute(self, base_ctx=None, **kwargs):  # pylint: disable = missing-function-docstring
      ctx = new_context(base_ctx, **kwargs)
      return get_context_return_tuple(ctx)

NODE_NAME = 'Context V2V // RvTools'
NODE_DESC = 'Context V2V'

NODE_CLASS_MAPPINGS = {
   NODE_NAME: RvPipe_Context_V2V
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}
