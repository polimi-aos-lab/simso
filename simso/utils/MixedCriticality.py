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

    def __str__(self):
        if self.value == 0:
            return 'LO'
        elif self.value == 1:
            return 'HI'

    @staticmethod
    def from_string(s):
        if s in ('LO'):
            return CritLevel.LO
        elif s in ('HI'):
            return CritLevel.HI
        else:
            raise NotImplementedError("Unsupported criticality level.")