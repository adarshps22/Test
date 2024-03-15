from enum import Enum

class TimeUnit(Enum):
    S = 1
    MS = 1000
    US = 1000000
    NS = 1000000000

    def __str__(self):
        return self.name.lower() 