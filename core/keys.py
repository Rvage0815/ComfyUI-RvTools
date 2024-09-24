﻿from enum import Enum


class TEXTS(Enum):
    CUSTOM_NODE_NAME = "RvTools"
    LOGGER_PREFIX = "rvtools"
    CONCAT = "concatenated"
    INACTIVE_MSG = "inactive"
    INVALID_METADATA_MSG = "Invalid metadata raw"
    FILE_NOT_FOUND = "File not found!"


class CATEGORY(Enum):
    MAIN = "👣 RvTools"
    CONVERSION = "/🧬 Conversion"
    FOLDER = "/📂 Folder"
    IMAGE = "/🖼️ Image"
    PASSER = "/👻 Passer"
    PIPE = "/🖇️ Pipe"
    PRIMITIVE = "/🦧 Primitives"
    SELECTOR = "/✔️ Selector"
    SETTINGS = "/⚙️ Settings"
    SWITCHES = "/🔌 Switches"
    MULTISWITCHES = "/🎛️ Switches (Multi)"
    TEXT = "/📝 Text"


# remember, all keys should be in lowercase!
class KEYS(Enum):
    LIST = "list_string"
    PREFIX = "prefix"
