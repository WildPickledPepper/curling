# -*- coding: utf-8 -*-

import socket
import time
import math
import argparse

# Connection key: Fill in according to the connection information given in the digital curling server interface.
# Note that this parameter will change every time the server is started.
key = "tewisfdlws_c38b4172-fcc9-4081-b6b2-ff5c60b37b91"
# Server host: Fill in according to the connection information given in the digital curling server interface.
host = 'curling-server-7788.jupyterhub.svc.cluster.local'
# Connection port: Fill in according to the connection information given in the digital curling server interface.
port = 7788

# Read host and port from call parameters
parser = argparse.ArgumentParser()
parser.add_argument('-H','--host', help='host', default=host, required=False)
parser.add_argument('-p','--port', help='tcp server port', default=str(port), required=False)
args, _ = parser.parse_known_args()

class AIRobot():
    def __init__(self, key, name, host, port, show_msg=False):
        # Create a new Socket object
        self.ai_sock = socket.socket()
        # Create Socket connection
        self.ai_sock.connect((host,port))
        print("已建立socket连接", host, port, flush=True)

        # Whether to display received/sent messages
        self.show_msg = show_msg
        # Send connection key
        self.send_msg("CONNECTKEY:" + key)

        # Set robot name
        self.name = name
        # Initialize curling position
        self.position = [0]*32
        # Initialize curling sport information
        self.motioninfo = [0]*5
        # Set the starting number of games
        self.round_num = 0

    # Send messages through socket objects
    def send_msg(self, msg):
        if (self.show_msg):
            print("  >>>> " + msg, flush=True)
        # Convert message data from string type to bytes type before sending
        self.ai_sock.send(msg.strip().encode())

    # Receive messages through socket objects and parse them
    def recv_msg(self):
        # In order to avoid the TCP sticky problem, every message sent by the digital curling server to the AI ​​player ends with 0 (a byte with a value of 0).
        # Here, the information is processed by receiving each byte one by one and then concatenating it. 0 is used as the information terminator between multiple pieces of information.
        buffer = bytearray()
        while True:
            # Receive 1 byte
            data = self.ai_sock.recv(1)
            # The loop is interrupted when empty data or information terminator (0) is received.
            if not data or data == b'\0':
                break
            # Splice current bytes into cache
            buffer.extend(data)
        # Convert message data from bytes type to string type and remove leading and trailing spaces
        msg_str = buffer.decode().strip()
        if (self.show_msg):
            print("<<<< " + msg_str, flush=True)

        # Separate message string into list with spaces
        msg_list = msg_str.split(" ")
        # The first item in the list is the message code
        msg_code = msg_list[0]
        # Subsequent items in the list are parameters
        msg_list.pop(0)
        # Return message code and message parameter list
        return msg_code, msg_list

    # Distance from base camp center
    def get_dist(self, x, y):
        House_x = 2.375
        House_y = 4.88
        return math.sqrt((x-House_x)**2+(y-House_y)**2)

    # Is there a pot in the base camp?
    def is_in_house(self, dist):
        House_R = 1.830
        Stone_R = 0.145
        if dist<(House_R+Stone_R):
            return 1
        else:
            return 0

    def recv_setstate(self, msg_list):
        # Current number of completed throws
        self.shot_num = int(msg_list[0])
        # Current number of completed games
        self.round_num = int(msg_list[1])
        # Total number of games
        self.round_total = int(msg_list[2])
        # Preparatory thrower (0 is the person holding the blue ball, 1 is the person holding the red ball)
        self.next_shot = int(msg_list[3])

    # Basic AI strategy
    def get_bestshot(self):
        if (self.show_msg):
            print("============第%d局第%d壶============" % (self.round_num+1, self.shot_num+1), flush=True)
        # Initialize the coordinate lists of the first-hand pot and the second-hand pot
        init_x, init_y, gote_x, gote_y = [0]*8, [0]*8, [0]*8, [0]*8
        # Initialize the curling ball information list in the base camp
        stone_in_house = []
        # Get information about curling balls in Base Camp
        for n in range(8):
            stone_is_init = True
            init_x[n], init_y[n] = float(self.position[n*4]), float(self.position[n*4+1])
            gote_x[n], gote_y[n] = float(self.position[n*4+2]), float(self.position[n*4+3])
            for (x, y) in [(init_x[n], init_y[n]), (gote_x[n], gote_y[n])]:
                distance = self.get_dist(x, y)
                if self.is_in_house(distance):
                    stone_in_house.append([distance, x, y, stone_is_init])
                stone_is_init = False

        # There is no ball in the base camp, hit the ball towards the center of the base camp
        if len(stone_in_house) == 0:
            shot_msg = "BESTSHOT 3.0 0 0"
        # There is a ball in the base camp
        else:
            stone_in_house=sorted(stone_in_house)
            _, x, y, stone_is_init = stone_in_house[0]
            # The ball closest to the center of the base camp is your own, protect it.
            if self.player_is_init == stone_is_init:
                v0 = 3.613 - 0.12234*y - 0.3
                h0 = x - 2.375
            # The ball closest to the center of the base camp belongs to the opponent and will be knocked away.
            else:
                v0 = 3.613 - 0.12234*y + 1
                h0 = x - 2.375
            shot_msg = "BESTSHOT " + str(v0) + " " + str(h0) + " 0"
        return shot_msg

    def get_sweep_distance(self):
        return None

    # Receive and process messages
    def recv_forever(self):
        # Empty message counter reset to zero
        retNullTime = 0
        self.on_line = True
        time0 = time.time()

        while(self.on_line):
            # Receive messages and parse them
            msg_code, msg_list = self.recv_msg()
            # If an empty message is received, the counter will be incremented by one.
            if msg_code == "":
                retNullTime = retNullTime + 1
            # Close the Socket connection if five empty messages are received
            if retNullTime == 5:
                break
            # If the message code is...
            if msg_code == "CONNECTNAME":
                if msg_list[0] == "Player1":
                    self.player_is_init = True
                    print("玩家1，首局先手", flush=True)
                else:
                    self.player_is_init = False
                    print("玩家2，首局后手", flush=True)
            if msg_code == "ISREADY":
                # Send "READYOK"
                self.send_msg("READYOK")
                time.sleep(0.5)
                # Send "NAME" and AI player name
                self.send_msg("NAME " + self.name)
                print(self.name +" 准备完毕！", flush=True)
            if msg_code == "NEWGAME":
                time0 = time.time()
            if msg_code=="SETSTATE":
                self.recv_setstate(msg_list)
            if msg_code=="POSITION":
                for n in range(32):
                    self.position[n] = float(msg_list[n])
            if msg_code == "GO":
                # Formulate strategies to generate betting information
                shot_msg = self.get_bestshot()
                # Send pot message
                self.send_msg(shot_msg)
            if msg_code == "MOTIONINFO":
                for n in range(5):
                    self.motioninfo[n] = float(msg_list[n])
                sweep_distance = self.get_sweep_distance()
                if sweep_distance is not None and sweep_distance > 0:
                    self.send_msg("SWEEP " + str(sweep_distance))
            # If notification is received that the opponent has violated the center line rule
            if msg_code == "CENTERLINE_VIOLATION":
                # The curling stone on the court is reset to the position before the opponent fouled
                self.send_msg("CENTERLINE_CHOICE RESET")
                # The curling stone maintains its current position on the court
                # self.send_msg("CENTERLINE_CHOICE KEEP")
            if msg_code == "SCORE":
                time1 = time.time()
                print("%s %s第%d局耗时%.1f秒" % (time.strftime("[%Y/%m/%d %H:%M:%S]"),self.name,self.round_num+1,time1-time0),
                      end=" ", flush=True)
                time0 = time1
                # Get score from message parameter list
                self.score = int(msg_list[0])
                # The team that scores goes first in the next game
                if  self.score > 0:
                    print("我方得"+str(self.score)+"分", end=" ", flush=True)
                    # If it is not infinite battle mode (fixed order)
                    if self.round_total != (-1):
                        self.player_is_init = True
                # The team that loses points will be the second player in the next game.
                elif self.score < 0:
                    print("对方得"+str(self.score*-1)+"分", end=" ", flush=True)
                    # If it is not infinite battle mode (fixed order)
                    if self.round_total != (-1):
                        self.player_is_init = False
                # If there is a draw, the order of the next game will be exchanged.
                else:
                    print("双方均未得分", end=" ", flush=True)
                    # If it is not infinite battle mode (fixed order)
                    if self.round_total != (-1):
                        self.player_is_init = not self.player_is_init
                if (self.player_is_init):
                    print("我方下局先手", flush=True)
                else:
                    print("我方下局后手", flush=True)
                # Every curling end starts from an empty sheet. Clear the
                # client-side cache immediately so no stale stones can leak
                # into the next decision while waiting for fresh POSITION and
                # SETSTATE messages from the server.
                self.position = [0] * 32
                self.motioninfo = [0] * 5
            # If the message code is "GAMEOVER"
            if msg_code == "GAMEOVER":
                if  msg_list[0] == "WIN":
                    print("我方获胜", flush=True)
                elif msg_list[0] == "LOSE":
                    print("对方获胜", flush=True)
                else:
                    print("双方平局", flush=True)

        # Close Socket connection
        self.ai_sock.close()
        print("已关闭socket连接", flush=True)

if __name__ == '__main__':
    # Initialize the AIRobot object
    airobot = AIRobot(key, name="CurlingAI", host=args.host, port=int(args.port))
    # The AIRobot object starts receiving and processing messages
    airobot.recv_forever()
