# dvr
Implementation of Distance Vector Routing Protocol via multi-threading in python,where each thread is an instance of a router and the threads communicate using a shared queue.
The input.txt file contains the input to the program.The format and the details of the input is as follows:
4
A B C D
A B 1
B C 1
C D 1
EOF
where:
● The first line represents the number of routers present in the network.
● The second line represents the fixed name (interface) of the router.
● The third line like "A B 1" represents the cost of link connecting nodes A and B. Similar semantics is followed until the last line.
● The last line represents the end of file (denoted by "EOF").
