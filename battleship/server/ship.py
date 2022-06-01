import json
import string
from abc import ABC

from battleship.config.config import Config
from battleship.server.direction import Direction
from battleship.server.position import Position


# check abastarct class
class Ship(ABC):
    def __init__(self) -> None:
        self.hits = 0

    def setID(self, id):
        self.id = id

    def getID(self):
        return self.id

    def isSunk(self):
        return self.hits >= self.width

    def setPosition(self, row, col):
        self.position = Position(row, col)

    def getPosition(self):
        return self.position

    def getWidth(self):
        return self.width

    def setWidth(self, width):
        self.width = width

    def addHit(self):
        self.hits += 1

    def setHits(self, value):
        self.hits = value

    def setDirection(self, direction: Direction):
        self.direction = direction

    def getDirection(self):
        return self.direction

    def getCoordinates(self):
        coordinates = set()
        if self.direction == Direction.HORIZONTAL:
            for col in range(self.position.COL, self.position.COL + self.width):
                coordinates.add((self.position.ROW, col))

        elif self.direction == Direction.VERTICAL:
            for row in range(self.position.ROW, self.position.ROW + self.width):
                coordinates.add((row, self.position.COL))

        return coordinates

    def convertToMap(self):
        shipDict = {}
        shipDict['row'] = self.position.ROW
        shipDict['col'] = self.position.COL
        shipDict['direction'] = self.direction.value
        shipDict['width'] = self.width
        shipDict['name'] = self.name
        shipDict['hits'] = self.hits

        return shipDict


class Destroyer(Ship):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Destroyer"
        self.width = int(Config.data['SHIPS']['destroyer'])


class Submarine(Ship):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Submarine"
        self.width = int(Config.data['SHIPS']['submarine'])


class Cruiser(Ship):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Cruiser"
        self.width = int(Config.data['SHIPS']['cruiser'])


class Battleship(Ship):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Battleship"
        self.width = int(Config.data['SHIPS']['battleship'])


class Carrier(Ship):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Carrier"
        self.width = int(Config.data['SHIPS']['carrier'])
