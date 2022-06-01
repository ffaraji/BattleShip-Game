import random
import threading
import time
from uuid import uuid4

from battleship.client.player import Player
from battleship.client.target import Target
from battleship.match.match import Match
from battleship.webService.app import app

# this test check accuracy of the scores
if __name__ == "__main__":
    print('# this test check accuracy of the scores')

    def f1():
        match = Match()
        match_key = str(uuid4())
        player_1_key = str(uuid4()) + '_1'
        player_2_key = str(uuid4()) + '_2'
        
        match.initNewMatch(match_key)
        while not match.isMatchFinished(match_key):
            (match.step(match_key, player_1_key, Target(random.randint(0, 9), random.randint(0, 9))))
            # time.sleep(1/3000)
            (match.step(match_key, player_2_key, Target(random.randint(0, 9), random.randint(0, 9))))
            # print('------------')

        player_1, player_2 = match.getScore(match_key)
        print('match id =', match_key, 'score : ', 'player_1 (', player_1, ':', player_2, ') player_2', ' ,rounds = ', match.getRound(match_key))
        list1, list2 = match.getShipList(match_key)
        print('player 2 ships sunk status: ', list1)
        print('player 1 ships sunk status: ', list2)
        # print(match.getRound(match_key))

    f1()