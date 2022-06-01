import random
import time
import requests

from battleship.client.attack import Attack
from battleship.client.target import Target
from battleship.match.hitResult import HitResult


class Player:
    def __init__(self, name) -> None:
        self.name = name

    def attack(self):
        target = self.calculateTarget()
        return target

    def updateStatus(self, attack: Attack, result: HitResult):
        print(f"{self.name} received result : {result}")
        self.status[attack.getRow()][attack.getCol()] = result

    def calculateTarget(self) -> Target:
        target_row = random.randint(0, self.fieldWidth - 1)
        target_col = random.randint(0, self.fieldHeight - 1)

        return Target(target_row, target_col)

    def start(self):
        # request for new game
        response = requests.post('http://localhost:5000/newmatch')
        data = (response.json())
        
        # recieve battleFiled Information
        self.fieldWidth = data['fieldWidth']
        self.fieldHeight = data['fieldHeight']

        # recieve match and player ID
        matchID = data['matchID']
        if 'playerID_1' in data:
            playerID = data['playerID_1']
        else:
            playerID = data['playerID_2']
            
        # create a field width * height
        self.status = [[0 for _ in range(self.fieldWidth)] for _ in range(self.fieldHeight)]
    
        # main loop for play
        while True:
            # get a target (for now is random)
            target = self.attack()

            # send to server
            response = requests.post('http://localhost:5000/attack', data={'matchID': matchID, 'playerID': playerID, 'row': target.row, 'col': target.col})
            print(response.text) # need to replace with log. this for test received response
            response = response.json()

            # check for game finish
            if response['hitResult'] == 'HitResult.MATCH_FINISHID':
                break

            # wait for a while to be his turn
            time.sleep(1/100)

        # request match score
        response = requests.post('http://localhost:5000/score', data={'matchID': matchID})
        response = (response.json())
        print(response)
