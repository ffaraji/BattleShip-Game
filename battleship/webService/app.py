import json
from uuid import uuid4
from flask import Flask, request

from battleship.client.target import Target
from battleship.database.redisCache import RedisCache
from battleship.match.match import Match

app = Flask(__name__)
db = RedisCache()

match = Match()

@app.route("/newmatch", methods=['post'])
def newMatch():
    keys = db.getLastGameKeys()

    # check the last game initilized info
    # each game needs for two player
    # if the last game has two players, then a new game init and send matchID and playerID to first player
    # if the last game has only one player then it means that no need to create new match and just send matchID to player_2
    if not keys or keys['playerID_2']:
        matchID = str(uuid4())
        player_1_ID = str(uuid4()) + '_1'
        player_2_ID = None
        fieldWidth, fieldHeight = match.initNewMatch(matchID)
        matchInfo = {'matchID':matchID, 'playerID_1': player_1_ID, 'fieldWidth': fieldWidth, 'fieldHeight': fieldHeight}
        db.dumpsLastGameKeys({'matchID':matchID, 'playerID_1': player_1_ID, 'playerID_2': None})
        return json.dumps(matchInfo)

    elif not keys['playerID_2']:
        player_2_ID = str(uuid4()) + '_2'
        fieldWidth, fieldHeight = match.getFieldBounderis(keys['matchID'])
        matchInfo = {'matchID': keys['matchID'], 'playerID_2': player_2_ID, 'fieldWidth': fieldWidth, 'fieldHeight': fieldHeight}
        db.dumpsLastGameKeys({'matchID': keys['matchID'], 'playerID_1': keys['playerID_1'], 'playerID_2': player_2_ID})
        return json.dumps(matchInfo)

    else:
        return 'ERROR', 400

@app.route("/attack", methods=['post'])
def handleAttack():
    matchID = request.form['matchID']
    playerID = request.form['playerID']
    row = request.form['row']
    col = request.form['col']
    hitResult = match.step(matchID, playerID, Target(int(row), int(col)))
    result = {'hitResult': str(hitResult), 'row': row, 'col': col, 'round = ': match.getRound(matchID)}
    return json.dumps(result)

@app.route("/round", methods=['post'])
def getRound():
    matchID = request.form['matchID']
    result = match.getRound(matchID)
    return str(result)

@app.route("/score", methods=['post'])
def getScore():
    matchID = request.form['matchID']
    result = match.getScore(matchID)
    return  json.dumps({'result': str(result)})
