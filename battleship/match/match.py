import random

from battleship.config.config import Config
from battleship.database.redisCache import RedisCache
from battleship.match.hitResult import HitResult
from battleship.server.board import BattleField
from battleship.server.direction import Direction
from battleship.server.ship import *


class Match:
    def __init__(self) -> None:
        self.config = Config()
        self.db = RedisCache()

    def initNewMatch(self, matchID):

        # init battle fields
        fieldWidth = int(self.config.data['MAP']['fieldwidth'])
        fieldHeight = int(self.config.data['MAP']['fieldheight'])
        
        # init ships and add to battleField
        for i in [1, 2]:
            battleField = BattleField(fieldWidth, fieldHeight)
            battleField.setMatchID(matchID)
            self.addShipsToField(battleField, Destroyer())
            self.addShipsToField(battleField, Submarine())
            self.addShipsToField(battleField, Cruiser())
            self.addShipsToField(battleField, Battleship())
            self.addShipsToField(battleField, Carrier())

            # save the initiated battlefield in to redis
            self.db.dumpBattleField(matchID, i, battleField)

        return fieldWidth, fieldHeight
            
    # try to find a random position for the ship in the battlefield
    # if there is a position which is not out of the battlefield
    # and it is not overlay on the other ships
    # then it place it in the battlefield
    # the loop will be continue untill to find a place
    # There maybe is a better sulosion than this one
    # needs to re check later 
    def addShipsToField(self, battleField, ship):
        # check corner edges
        # check infinity loop (map size )
        while True:
            direction = random.choice(
                [Direction.HORIZONTAL, Direction.VERTICAL]
            )  
            row = random.randint(0, battleField.fieldHeight - 1)
            col = random.randint(0, battleField.fieldWidth - 1)

            if battleField.canPlaceShip(row, col, ship.width, direction):
                ship.setPosition(row, col)
                ship.setDirection(direction)
                battleField.placeShip(ship)
                break

    def initNewMatchManualy(self, matchID):

        # init battle fields
        fieldWidth = int(self.config.data['MAP']['fieldwidth'])
        fieldHeight = int(self.config.data['MAP']['fieldheight'])
        
        # init ships and add to battleField
        for i in [1, 2]:
            battleField = BattleField(fieldWidth, fieldHeight)
            battleField.setMatchID(matchID)
            self.addShipsToFieldManualy(battleField, Destroyer(), 0, 0, Direction.HORIZONTAL)
            self.addShipsToFieldManualy(battleField, Submarine(), 1, 0, Direction.HORIZONTAL)
            self.addShipsToFieldManualy(battleField, Cruiser(), 2, 0, Direction.HORIZONTAL)
            self.addShipsToFieldManualy(battleField, Battleship(), 3, 0, Direction.HORIZONTAL)
            self.addShipsToFieldManualy(battleField, Carrier(), 4, 0, Direction.HORIZONTAL)
            self.db.dumpBattleField(matchID, i, battleField)

        return fieldWidth, fieldHeight

    def addShipsToFieldManualy(self, battleField, ship, row, col, direction):
        # check corner edges
        # check infinity loop (map size )
        ship.setPosition(row, col)
        ship.setDirection(direction)
        battleField.placeShip(ship)

    def getFieldBounderis(self, matchID):
        battleField = self.db.loadBattleField(matchID, 1)
        return battleField.fieldWidth, battleField.fieldHeight

    def isMatchFinished(self, matchID):
        battleField_1 = self.db.loadBattleField(matchID, 1)
        battleField_2 = self.db.loadBattleField(matchID, 2)
        field_1_all_ships_sunk = all([ship.isSunk() for ship in battleField_1.getShips()])
        field_2_all_ships_sunk = all([ship.isSunk() for ship in battleField_2.getShips()])
        isPlayers_turn_complete = not (self.db.getRound(matchID) % 2)
        return (field_1_all_ships_sunk or field_2_all_ships_sunk) and isPlayers_turn_complete

    def getShipList(self, matchID):
        battleField_1 = self.db.loadBattleField(matchID, 1)
        battleField_2 = self.db.loadBattleField(matchID, 2)
        list1 = [ship.isSunk() for ship in battleField_2.getShips()]
        list2 = [ship.isSunk() for ship in battleField_1.getShips()]
        return(list1, list2)

    def getRound(self, matchID):
        return self.db.getRound(matchID)

    def getScore(self, matchID):
        battleField_1 = self.db.loadBattleField(matchID, 1)
        battleField_2 = self.db.loadBattleField(matchID, 2)
        player_1_score = sum([ship.isSunk() for ship in battleField_2.getShips()])
        player_2_score = sum([ship.isSunk() for ship in battleField_1.getShips()])
        return player_1_score, player_2_score

    def checkPlayerTurn(self, matchID, playerID):
        return self.db.getRound(matchID) % 2 != int(playerID[-1]) % 2

    # to find the opponent player identification (last caracter of the player id)
    # it is used to load opponent player battlefield and ships
    def getReverseSeqID(self, playerID):
        return 1 if int(playerID[-1]) == 2 else 2

    def getSeqID(self, playerID):
        return int(playerID[-1])

    # process attack request
    def step(self, matchID, playerID, target):
        # check match finished
        if self.isMatchFinished(matchID):
            return HitResult.MATCH_FINISHID

        # check player turn
        if not self.checkPlayerTurn(matchID, playerID):
            return HitResult.NOT_YOUR_TURN

        # move forward round by one
        self.db.moveForwardRound(matchID)

        # load (opponent) battleField from db
        seqID = self.getReverseSeqID(playerID)
        battleField = self.db.loadBattleField(matchID, seqID)

        # apply attack
        hitResult = battleField.applyAttack(matchID, playerID, target)

        # dump battle field to db
        self.db.dumpBattleField(matchID, seqID, battleField)

        return hitResult

