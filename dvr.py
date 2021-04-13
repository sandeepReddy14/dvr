import time
import threading
import queue
import math
import sys

lock=threading.Lock()

file_name=sys.argv[1]
#reading input from file.
try:
    file=open(file_name,"r")
except FileNotFoundError:
    print("File not found")
    sys.exit(0)

router_count=int(file.readline())
routers=file.readline().split()
#dictionary to store routers with name as key and id as value
d={}
#dictionary to store routers with id as key and name as value
d_rev={}
for i in range(router_count):
    d[routers[i]]=i
    d_rev[i]=routers[i]

#matrix to store the weights
matrix=[]
for i in range(router_count):
    a=[]
    for j in range(router_count):
        if i==j:
            a.append(0)
        else:
            a.append(math.inf)
    matrix.append(a)

for line in file:
    if line!="EOF\n":
        src,dest,cost=line.split()
        cost=int(cost)
        matrix[d.get(src)][d.get(dest)]=cost
        matrix[d.get(dest)][d.get(src)]=cost

file.close()

#shared queue for communication between threads
shared_queue=[]
for i in range(router_count):
    q=queue.Queue()
    shared_queue.append(q)

#utility functions
def print_routing_table(destination,cost,next_hop,check):
    print("-------------------------")
    print("Dest\tcost\tNext hop")
    for i in range(router_count):
        if(check[i]):
            print("-------------------------")
            if cost[i]==math.inf:
                print(destination[i]+"\t"+str(cost[i])+"\t"+"-"+"  *")
            else:
                print(destination[i]+"\t"+str(cost[i])+"\t"+next_hop[i]+"  *")
        else:
            print("-------------------------")
            if cost[i]==math.inf:
                print(destination[i]+"\t"+str(cost[i])+"\t"+"-")
            else:
                print(destination[i]+"\t"+str(cost[i])+"\t"+next_hop[i])
    print("-------------------------")
    print()

#function for router instance
def create_router(name):
    global iteration
    router_name=name
    routing_table=[]
    destination=[]
    cost=[]
    next_hop=[]
    check=[]
    neighbours=[]
    for i in range(router_count):
        destination.append(routers[i])
        cost.append(matrix[d.get(router_name)][i])
        next_hop.append(routers[i])
        check.append(False)
    routing_table.append(destination)
    routing_table.append(cost)
    routing_table.append(next_hop)

    #routing_table=[destination,cost,next_hop]
    index=d.get(router_name)
    for i in range(router_count):
        if matrix[index][i]!=math.inf:
            neighbours.append(d_rev.get(i))
    neighbours_length=len(neighbours)
    lock.acquire()
    print("Routing table at ",router_name)
    print_routing_table(destination,cost,next_hop,check)
    lock.release()

    count=1
    while count!=router_count-1:
        time.sleep(0.5)
        lock.acquire()
        if count==iteration:
            print("Iteration number : "+str(count))
            print()
            iteration+=1
        count+=1
        lock.release()
        for i in range(router_count):
            check[i]=False
        for node in neighbours:
            shared_queue[d.get(node)].put((router_name,cost,destination))
        while(shared_queue[d.get(router_name)].qsize()!=neighbours_length):
            continue
        while(shared_queue[d.get(router_name)].empty()==False):
            buffer=shared_queue[d.get(router_name)].get()
            for i in range(router_count):
                if(buffer[0]!=router_name and routers[i]!=buffer[0]):
                    if(buffer[1][i]+cost[d.get(buffer[0])]<cost[i]):
                        cost[i]=buffer[1][i]+cost[d.get(buffer[0])]
                        next_hop[i]=buffer[0]
                        check[i]=True
        time.sleep(2)
        lock.acquire()
        print("Routing table at ",router_name)
        print_routing_table(destination,cost,next_hop,check)
        lock.release()
iteration=1
#creating threads
for i in range(router_count):
    thread=threading.Thread(target=create_router,args=(routers[i],))
    thread.start()
