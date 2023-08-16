import socket
import random
import threading

range_diff = random.randint(10**4, 10**5)
start_point = random.randint(0, 10**5 - range_diff)
l = start_point
r = start_point + range_diff
x = random.randint(l, r)
order_of_escape = []
print_lock = threading.Lock()

def main():
    num_player = int(input("Enter the number of players: "))
    s = socket.socket()
    print("Socket created")

    s.bind(('localhost', 31009))
    s.listen(num_player)
    print("Waiting for connections")

    print("l:", l)
    print("r:", r)
    print("rd:", range_diff)
    print("X:", x)

    barrier = threading.Barrier(num_player + 1)

    threads = []
    for i in range(num_player):
        c, address = s.accept()
        thread = threading.Thread(target=handle_client, args=(c, address, barrier))
        thread.start()
        threads.append(thread)

    barrier.wait()  
    send_range_data(threads)  

    for thread in threads:
        thread.join()

def send_range_data(threads):
    data = str(l) + '|' + str(r)
    for thread in threads:
        c = thread._args[0] 
        c.send(bytes(data, 'utf-8'))

def handle_client(c, address, barrier):
    name2 = c.recv(1024).decode()
    with print_lock:
        print("Client connected", address, name2)

    barrier.wait() 

    while True:
        y = int(c.recv(1024).decode())
        with print_lock:
            print("Received guess from client:", name2, y)
            print("Sending response to client:", name2)
        if y > x:
            c.send(bytes('Value too high', 'utf-8'))
        elif y < x:
            c.send(bytes('Value too low', 'utf-8'))
        else:
            c.send(bytes('Correct guess', 'utf-8'))
            order_of_escape.append(name2)
            break
    c.close()

if __name__ == "__main__":
    main()
    print("Order of escape:")
    for i in range(len(order_of_escape)):
        print(i + 1, order_of_escape[i])
