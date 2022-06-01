import json
import redis

from battleship.client.target import Target
from battleship.config.config import Config
from battleship.server import direction
from battleship.server.board import BattleField
from battleship.server.direction import Direction
from battleship.server.ship import Ship


class RedisCache:

    # singleton
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(RedisCache, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self) -> None:
        try:
            config = Config()
            host = config.data['REDIS']['host']
            port = int(config.data['REDIS']['port'])
            db = int(config.data['REDIS']['db'])
            self.redis = redis.Redis(host=host, port=port, db=db)
            # self.redis.ping()
        except Exception as e:
            print('Redis config not exist....', e)
            
    def isTargetInHits(self, matchID, playerID, target: Target):
        seqID = playerID[-1]
        key = matchID + '_battleField_' + str(seqID) + '_Hits'
        
        if self.redis.sismember(key, str((target.row, target.col))):
            return True
        
        return False

    def addTargetToHits(self, matchID, playerID, target: Target):
        seqID = playerID[-1]
        key = matchID + '_battleField_' + str(seqID) + '_Hits'
        
        self.redis.sadd(key, str((target.row, target.col)))

    def loadShips(self, matchID, seqID):
        key = matchID + '_battleField_' + str(seqID) + '_ships'

        data = self.redis.get(key)
        ships = json.loads(data)

        shipList = []
        for jship in ships:
            ship = Ship()
            ship.setPosition(int(jship['row']), int(jship['col']))
            dir = Direction.HORIZONTAL if int(jship['direction']) == 0 else Direction.VERTICAL
            ship.setDirection(dir)
            ship.setWidth(int(jship['width']))
            ship.name = jship['name']
            ship.setHits(int(jship['hits']))

            shipList.append(ship)

        return shipList

    def dumpShips(self, matchID, seqID, ships):
        key = matchID + '_battleField_' + str(seqID) + '_ships'
        shipList = []
        for ship in ships:
            shipList.append(ship.convertToMap())
        
        self.redis.set(key, json.dumps(shipList))
        

    def dumpBattleField(self, matchID, seqID, battleField: BattleField):
        key = matchID + '_battleField_' + str(seqID)
        battleField_dict = {'width': battleField.fieldWidth, 'height': battleField.fieldHeight}
        self.redis.hmset(key, battleField_dict)

        self.dumpShips(matchID, seqID, battleField.ships)

    def loadBattleField(self, matchID, seqID):
        key = matchID + '_battleField_' + str(seqID)
        fieldWidth = self.redis.hget(key, 'width')
        fieldHeight = self.redis.hget(key, 'height')
        
        battleField = BattleField(int(fieldWidth), int(fieldHeight))
        battleField.setMatchID(matchID)  

        ships = self.loadShips(matchID, seqID)
        for ship in ships:
            battleField.addShip(ship)
        return battleField      

    def moveForwardRound(self, matchID):
        key = matchID + '_round'
        round = self.redis.get(key)
        round = 1 if round is None else int(round) + 1
        self.redis.set(key, round)

    def getRound(self, matchID):
        key = matchID + '_round'
        round = self.redis.get(key)
        
        return 0 if round is None else int(round)


    def getLastGameKeys(self):
        key = 'BattleShip_LastMatch_keys'
        data = self.redis.get(key)

        return json.loads(data) if data else None

    def dumpsLastGameKeys(self, matchKeys):
        key = 'BattleShip_LastMatch_keys'
        matchKeys = json.dumps(matchKeys)
        self.redis.set(key, matchKeys)