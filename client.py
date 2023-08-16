import socket
import random

class Prisoner:
    def __init__(self, name):
        self.name = name
    
    def play_game(self):
        c = socket.socket()
        c.connect(('localhost', 31009))

        c.send(bytes(self.name, 'utf-8'))

        data = c.recv(1024).decode()
        l, r = map(int, data.split('|'))
        # print(f"Received range for {self.name}: {l} - {r}")

        while True:
            y = random.randint(l, r)
            # print(f"{self.name} sending guess: {y}")
            c.send(bytes(str(y), 'utf-8'))

            data2 = c.recv(1024).decode()
            # print(f"{self.name} received response: {data2}")

            if data2 == 'Correct guess':
                c.close()
                # print(self.name, "escaped")
                break
            elif data2 == 'Value too low':
                l = y 
            else:
                r = y 

        c.close()
name=input("enter prisoner name")
prisoner = Prisoner(name)
prisoner.play_game()
