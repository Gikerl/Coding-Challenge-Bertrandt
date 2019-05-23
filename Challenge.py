import time as Timer 
import json

#Timer
startTimer = int(round(Timer.time() * 1000))

#Global Const
StartNodeLabel = "Erde"
TargetNodeLabel = "b3-r7-r4nd7"
FilePath = "generatedGraph.json"

#Global Var
Data = {}
Matrix = []
Length = 0
StartNode = 0
TargetNode = 0

#Read Json File 
with open(FilePath) as jFile:  
    Graph = json.load(jFile)

#Find Start/Target Node Indices
for i in range(0, len(Graph["nodes"])):
    if Graph["nodes"][i]["label"] == StartNodeLabel:
        StartNode = i
    elif Graph["nodes"][i]["label"] == TargetNodeLabel:
        TargetNode = i
        
#Matrix Size
Length = len(Graph["nodes"])

#Tranform Graph into better DataStructure
def FindConnections(index):
    connections = {}
    for e in range(0, len(Graph["edges"])):
        if Graph["edges"][e]["source"] == index:
            connections[Graph["edges"][e]["target"]] = Graph["edges"][e]["cost"]
    return connections

for n in range(0, Length):
    Data[n] = FindConnections(n)
    
#Create Matrix
for y in range(0, Length):
    row = []
    for x in range(0, Length):
        row.append(0)
    Matrix.append(row)
    
#Fill Matrix (symmetrically)
for n, v in Data.items():
    for t,c in v.items():
        Matrix[n][t] = c
        Matrix[t][n] = c

#Helper Methode        
def GetConnections(y):
    connections = {}
    for x in range(0, Length):
        if Matrix[y][x] > 0:
            connections[x] = Matrix[y][x]
    return connections
    
    
#Find Shortest Path (Dijkstra Approach)
Queue = [(StartNode, 0, -1)] #Initial Queue
Visited = {}

def GetShortestPath(index, distance, path):
    Visited[index] = (distance, path)
    c = GetConnections(index)
    for k, v in c.items():
        if k not in Visited:
            if k not in Queue:
                Queue.append((k, v+distance, index)) #Start Queue
            else:
                for i, q in enumerate(Queue):
                    if q[1] > v: #Insert Sorted
                        Queue.insert(i, (k, v+distance, index))
                        break
                    if i == len(Queue)-1: #Insert as Last element
                        Queue.append((k, v+distance, index))
                        break

while True:
    s = Queue[0]
    Queue.pop(0)
    GetShortestPath(s[0], s[1], s[2])
    
    #No Path To Target
    if len(Queue) == 0:
        print("No Path To Target Possible!")
        print("Aborting!")
        exit()
    
    #Target Reached?
    if(s[0]==TargetNode):
        break

Path = [TargetNode]
def BackTracePath(node):
    return Visited[node][1]
    
while True:
    p = BackTracePath(Path[0])
    Path.insert(0, p)
    #Start Reached?
    if(p == StartNode):
        break

LabeledPath = []
for p in Path:
    LabeledPath.append(Graph["nodes"][p]["label"])

#Results
print('Distance from \"{}\" to \"{}\": {}'.format(StartNodeLabel, TargetNodeLabel, Visited[TargetNode][0]))
print("Path taken: " + ', '.join(LabeledPath))
print('Script Execution Time: {}'.format((int(round(Timer.time() * 1000)) - startTimer) / 1000))