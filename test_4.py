from sklearn.compose import TransformedTargetRegressor
from battleship.client.player import Player
import threading

if __name__ == "__main__":

    def f():
        player = Player()
        player.start()


    for i in range(2):
        t = threading.Thread(target=f)
        t.start()