import random
import threading
import time
from uuid import uuid4

from battleship.client.player import Player
from battleship.client.target import Target
from battleship.match.match import Match
from battleship.webService.app import app

# this test test cuncurent multiple match capability 
if __name__ == "__main__":
    print('this test test cuncurent multiple match capability ')
    def f1():
        match = Match()
        match_key = str(uuid4())
        player_1_key = str(uuid4()) + '_1'
        player_2_key = str(uuid4()) + '_2'
        
        match.initNewMatch(match_key)
        while not match.isMatchFinished(match_key):
            (match.step(match_key, player_1_key, Target(random.randint(0, 9), random.randint(0, 9))))
            
            (match.step(match_key, player_2_key, Target(random.randint(0, 9), random.randint(0, 9))))
            

        print('match id =', match_key, 'score = ', match.getScore(match_key), 'rounds = ', match.getRound(match_key))
        

    for i in range(4):
        t1 = threading.Thread(target=f1)
        t1.start()
        time.sleep(1/100)