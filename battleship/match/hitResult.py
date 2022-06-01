from enum import Enum


class HitResult(Enum):
    MISS = 0
    HIT = 1
    DESTROYED = 2
    OUT_OF_BOUND = 3
    REPETITIVE = 4
    NOT_YOUR_TURN = 5
    MATCH_FINISHID = 6
