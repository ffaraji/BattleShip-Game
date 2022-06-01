import random
import threading
import time
from uuid import uuid4

from battleship.client.player import Player
from battleship.client.target import Target
from battleship.match.match import Match
from battleship.webService.app import app

''''
 this test check MISS, HIT, OUTBOUND

 ships are at the following points:
 Destroyer withds 2: (0,0), (0,1)
 Submarine withds 3: (1,0), (1,1), (1,2)
 Cruiser withds 3: (2,0), (2,1), (2,2)
 Battleship withds 4: (3,0), (3,1), (3,2), (3,3)
 Carrier withds 5: (4,0), (4,1), (4,2), (4,3), (4,4)

 Any attack to the above point return Hit
 Any attack other point return MISS
 When all points of a ship hited returns DESTROYED
 Any attack othr point outside the field return OUT_OF_BOUND (width 0 ~ 9) (height 0 ~ 9)
 Any attack to previously atacked point return REPETITIVE
'''

if __name__ == "__main__":
    print('This test check MISS, HIT, OUTBOUND, target = ships points')

    def f1():
        match = Match()
        match_key = str(uuid4())
        player_1_key = str(uuid4()) + '_1'
        player_2_key = str(uuid4()) + '_2'
        
        match.initNewMatchManualy(match_key)

        # test HIT, DESTROYED
        print('test HIT, DESTROYED')
        targets = [(0, 0), (0, 1), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2), (3,0), (3,1), (3,2), (3,3), (4,0), (4,1), (4,2), (4,3), ]
        for target in targets:
            attackResult = match.step(match_key, player_1_key, Target(target[0], target[1]))
            print(attackResult)

        print('-------------------------------------------')
        print('This test check MISS and REPETITIVE target = (8,8)')
        for _ in range(5):
            attackResult = match.step(match_key, player_1_key, Target(8,8))
            print(attackResult)

        print('-------------------------------------------')
        print('This test check OUT_OF_BOUND target = (10,8)')
        attackResult = match.step(match_key, player_1_key, Target(10,8))
        print(attackResult)

    f1()