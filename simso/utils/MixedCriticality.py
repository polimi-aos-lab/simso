from enum import Enum
from functools import total_ordering

@total_ordering
class CritLevel(Enum):
    LO = 0
    HI = 1

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    @staticmethod
    def from_string(s):
        if s in ('LO'):
            return CritLevel.LO
        elif s in ('HI'):
            return CritLevel.HI
        else:
            raise NotImplementedError("Unsupported criticality level.")