import string

from battleship.client.target import Target
from battleship.database import redisCache
from battleship.match.hitResult import HitResult
from battleship.server.direction import Direction
from battleship.server.ship import Ship


class BattleField:
    def __init__(self, height=10, width=10) -> None:
        self.fieldWidth = width
        self.fieldHeight = height
        self.ships = []
        self.db = redisCache.RedisCache()

    def setMatchID(self, id):
        self.matchID = id

    def getShips(self):
        return self.ships
    
    def placeShip(self, ship: Ship):
        self.addShip(ship)

    # check if a new ship can place in a position
    # check for out of bound and overlay with other ships
    def canPlaceShip(self, row, col, shipWidth, direction):
        if direction == Direction.HORIZONTAL:
            # out of bound check
            if col + shipWidth - 1 not in range(0, self.fieldWidth):
                return False
            # overlay with other ships check
            for n in range(col, col + shipWidth):
                for ship in self.ships:
                    if (row, n) in ship.getCoordinates():
                        return False

            return True

        elif direction == Direction.VERTICAL:
            # out of bound check
            if row + shipWidth - 1 not in range(0, self.fieldHeight):
                return False

            # overlay with other ships check
            for n in range(row, row + shipWidth):
                for ship in self.ships:
                    if (n, col) in ship.getCoordinates():
                        return False

            return True

        return False

    def addShip(self, ship: Ship):
        self.ships.append(ship)

    def checkBounderis(func):
        def wraper(self, *args):
            if args[2].getRow() in range(0, self.fieldWidth) \
             and args[2].getCol() in range(0, self.fieldHeight):
                return func(self, *args)
            else:
                return HitResult.OUT_OF_BOUND

        return wraper

    # using decorators to check target to be inside field
    @checkBounderis
    def applyAttack(self, matchID: string, playerID: string, target: Target) -> HitResult:
        # check redis for including target or not
        if self.db.isTargetInHits(matchID, playerID, target):
            return HitResult.REPETITIVE

        # add target to redis set
        self.db.addTargetToHits(matchID, playerID, target)

        for ship in self.ships: 
            if (target.row, target.col) in ship.getCoordinates():
                ship.addHit()
                if ship.isSunk():
                    return HitResult.DESTROYED
                else:
                    return HitResult.HIT

        return HitResult.MISS
