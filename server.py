import socket
import threading

IP="localhost"
PORT=12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024) 
server_socket.bind(("localhost", 12345)) 
server_socket.listen(5) 
print(f"{IP}:{PORT} has binded")

mass_clients={}
start=True
i=0
message=""


def start_to_users():
    a=i-1
    global message
    mess=""
    try:
        while mass_clients[a]['Start']:
            if mess != message:
                mass_clients[a]['client'].sendall(f"{message}".encode('utf-8'))
                mess=message
    except ConnectionResetError as e:
        mass_clients[a]['Start']=False

def run_server_cods():
    global message
    a=i-1
    try:
        while mass_clients[a]['Start']:
            data = mass_clients[a]['client'].recv(1024).decode('utf-8')
            if not data:
                break
            io=data.split(":")
            if io[0]=="Name":
                mass_clients[a]['Name']=io[1]
                # message=mass_clients[a]['Name']+":ni9uwGTy0zZak89zcEwvb6XAy4Pnsrmi7eHc6AyNuKqHS8z4sliw6bHM0Fk81ggKtQjSstmOq0pRVLc1Ejx5Mzq0unFnbvjXSJyv"
                message=mass_clients[a]['Name']+" connected to chat"
            else:
                message=mass_clients[a]['Name']+":"+data.split(":")[1]
            # print(data)
            pass
    except ConnectionResetError as e:
        mass_clients[a]['Start']=False
        # message=f"{mass_clients[a]['Name']}jOxfdTwSmNlfwGlSpHfshRgvW8IHJCkRagQ3sfQpOIwS0FFJkZSD7V3UH17OL2yHoOBxFnGuePynI0FAHfqb6buzZXed6BzlgT45"
        message=mass_clients[a]['Name']+" disconected in chat"

try:
    while True:
        client_socket, addr = server_socket.accept()
        # print(f"Connected by {addr}")
        i=i+1
        threads=threading.Thread(target=start_to_users,daemon=True)
        thread=threading.Thread(target=run_server_cods,daemon=True)
        mass_clients[i-1]={'client':client_socket,'addr':addr,'thread':thread,'thread_message':threads,'Name':"",'Start':True}
        threads.start()
        thread.start()

        

finally:
    start=False
    for i in range(len(mass_clients)):
        mass_clients[i]['thread'].join()
    server_socket.close()
    print("Server stopped.")