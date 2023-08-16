#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from std_msgs.msg import Float32MultiArray 

class ServerNode:
    def __init__(self):
        rospy.init_node('server_node')
        self.subscriber_a = rospy.Subscriber('server_a', String, self.callback,callback_args=('a'))
        self.subscriber_b = rospy.Subscriber('server_b', String, self.callback,callback_args=('b'))
        self.publisher_turn = rospy.Publisher('turn', String, queue_size=10)
        self.publisher_hp = rospy.Publisher('hp',Float32MultiArray, queue_size=10)
        self.rate =rospy.Rate(1)
        self.max_hp = {"fire":300,"water" :400,"earth": 500, "rock" :300, "thunder": 400, "wind": 500}
        self.hp=[300,400,500,300,400,500]
        self.current_turn='a'
        self.rounds=0
        self.sent_once= True
        
    
    def send_hp(self):
        hp_msg=Float32MultiArray()
        hp_msg.data = self.hp
        self.publisher_hp.publish(hp_msg)
        
        
    def send_turn(self):
        if self.current_turn == 'a turn':
            self.current_turn = 'b turn'
        else:
            self.current_turn = 'a turn'
        turn_msg = String()
        turn_msg.data=self.current_turn
        self.publisher_turn.publish(turn_msg)
        self.rounds += 1
        
        
    def cal_hp(self, msg, player):
        msg= msg.split()
        for i in range(len(msg)):
            if msg[i] == '1':
                hp_reduction=self.max_hp[msg[i-1]] * 0.1
                if player == 'a':
                    for j in range(3, 6):
                        self.hp[j] -= hp_reduction
                elif player == 'b':
                    for j in range(3):
                        self.hp[j] -= hp_reduction
            elif msg[i] == '2' and i+1 < len(msg):
                name = msg[i+1]
                hp_reduction = self.max_hp[msg[i-1]] * 0.2
                if player == 'a':
                    if name == 'rock':
                        self.hp[3] -= hp_reduction
                    elif name == 'thunder':
                        self.hp[4] -=  hp_reduction
                    elif name == 'wind':
                        self.hp[5] -=  hp_reduction
                elif player == 'b':
                    if name == 'fire':
                        self.hp[0] -=  hp_reduction
                    elif name == 'water':
                        self.hp[1] -=  hp_reduction
                    elif name == 'earth':
                        self.hp[2] -=  hp_reduction
        for i in range(6):
            if self.hp[i] < 0:
                self.hp[i] = 0

    def callback(self, data,args):
        player = args
        print(f"RECEIVED FROM {player}")
        self.print_message(data.data)
        self.cal_hp(data.data,player)
        self.send_hp()
        self.send_turn()
        
    # def callback_b(self, data):
    #     print(f"Received from Client B: {data.data}")
    #     self.cal_hp(data.data,'b')
    #     self.send_hp()
    #     self.send_turn()
    def print_message(self,msg):
        msg = msg.split()
        i = 0
        while i < len(msg):
            if msg[i] == "1":
                print("attacked all")
            elif msg[i] == "2":
                print("attacked", msg[i + 1])
                i += 1
            else:
                print(msg[i], end=" ")
            i += 1
        
            
    def check_winner(self):
        if all(h == 0 for h in self.hp[3:]):
            self.publisher_turn.publish("A won \nB lost")
            rospy.signal_shutdown("Game over")
        elif all(h == 0 for h in self.hp[:3]):
            self.publisher_turn.publish("B won \nA lost")
            rospy.signal_shutdown("Game over")

    def run(self):
        while not rospy.is_shutdown():
            if self.publisher_hp.get_num_connections()==2 and self.publisher_turn.get_num_connections()==2 and self.sent_once :
                self.send_hp()
                self.send_turn()
                self.sent_once = False
            self.check_winner()
            self.rate.sleep()
       

if __name__ == '__main__':
    server_node = ServerNode()
    server_node.run()
