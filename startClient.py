import sys
from battleship.client.player import Player


if __name__ == "__main__":
    player = Player(sys.argv[1])
    player.start()
