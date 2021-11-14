from dataclasses import dataclass
from dataclasses import field
import dataclasses
from enum import IntEnum

class CommandType(IntEnum):
    REGISTER = 1
    UNREGISTER = 2

@dataclass
class ManagerCommand:
    type: CommandType
    payload: any
    