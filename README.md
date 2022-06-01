# battleship
This battleShip game is written in scalable cloud-native approach.

Any number of users can connect to the server. For each game, two users will be assigned.

All the game status and data is kept in Redis database. So it means that any number of replicas form the server instanse will be OK.

Each user connection and request can be sent to any instance or pod. So LoadBalancing is easy.

Currently, users(clients) can send thier requests in Rest format.
All the requests are post.
A user can send /newmatch request to start a game. A matchID and PlayerID then return to user. Theise IDs should be submitted with each request then.

User can check their turn by sending multiple /attack request. This will be fixed latter by applying HTTP2 protocol.

Users receive their attack response in the following format:
[HitResult, row, col, round]
row and col are the submitted points by user

HitResult is as bellow:

HitResult.MISS

HitResult.HIT

HitResult.DESTROYED

HitResult.OUT_OF_BOUND

HitResult.REPETITIVE

HitResult.NOT_YOUR_TURN

HitResult.MATCH_FINISHID

Users can get match score by sending /score request

# Run Server
To run server inside a container run the following command:

docker-compose up

To run server without docker, you need to modify the mapconfig.conf file inside config directory as follow:
Under the [REDIS] section, change the host to 'localhost'

Then run the following command:

python3 startServer.py

# Run Sample Client
To run a sample client, you need to run the following command:

python3 startClient.py

This sample client is a dummy client and send random targets to server

# Run tests
Under the test branch, there are some test files like test_1.py.
These tests are unit tests and test different parts of server.

# Future works
HTTP2 with header load balancing for in memory (in POD) cache

websocket

logging, monitoring



