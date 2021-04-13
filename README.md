# dvr algortihm also know as Bellman-Ford Algorithm
Implementation of Distance Vector Routing Protocol algorithm via multi-threading in python,where each thread is an instance of a router and the threads communicate using a shared queue.<br>

To run the program use:<br>
`python3 dvr.py testcase.txt`<br>
The input.txt file conatins the input to the program.The format and the details of the input is as follows:<br>

4<br>
A B C D<br>
A B 1<br>
B C 1<br>
C D 1<br>
EOF<br>

Where:<br>
● The first line represents the number of routers present in the network.<br>
● The second line represents the fixed name (interface) of the router.<br>
● The third line like "A B 1" represents the cost of link connecting nodes A and B. Similar semantics is followed until the last line.<br>
● The last line represents the end of file (denoted by "EOF").<br>
