import sys

class Node:
    neighbours = []
    name = ""
    def __init__ (self, nodeName):
        self.name = nodeName
        self.neighbours = []

class MyPriorityQueue(object):
    queue = []
    def __init__ (self):
        self.queue = []

    def getQueueLength(self):
        return len(self.queue)

    def addElement(self, node):
        if (node not in self.queue):
            self.queue.append(node)
            if len(self.queue) == 1:
                return self.queue
            else:
                index = len(self.queue) -1
                finished = False
                while finished == False:
                    if index - 1 > -1:
                        if len(self.queue[index].neighbours) < len(self.queue[index -1].neighbours):
                            previous = self.queue[index -1]
                            self.queue[index -1] = self.queue[index]
                            self.queue[index] = previous
                            index = index -1
                        else:
                            finished = True
                    else:
                        finished = True		
        return self.queue

    def	 takeElementWithLowestK(self):
        if len(self.queue) > 0:
            nodeToReturn = self.queue[0]
            self.queue.remove(self.queue[0])
            
            return nodeToReturn
    def rearrange (self, node):
        if (node in self.queue):
            self.queue.remove(node)
            self.addElement(node)


def MyOpenFile(path, text): # Function that opens a file at location "path" and returns the text specified. If locating the file fails, user is asked to try again 

    try: # if file at location "path" opened sucessfully 
        with open(path, "r") as graphFile:			
            # take all the lines from the file and save them to the "text" var
            text = graphFile.readlines()
            graphFile.close()
            return text   
    except FileNotFoundError: # if file at location "path" fails to open
        print("file could not be opened")
        print("Write the full path of the file that contains the graph")
        path = input("") #save new path inserted from user
        return MyOpenFile(path, text) # try again to open file	

#function that takes as parameters: the line that contains the new combination and a list with the nodes that we want to add the new node(s) and transitions
#The form of the line should be like that: "StartingNodeName EndingNodeName"
def createGraphFromText (textLine, listOfTotalNodes):
    data = textLine.split(" ") # split the line for every "space" there is. Store the devided elements to array "data". The first shell should contain the startingNodeName and the second the EndingNodeName
    if data is not None:
        if len(data) > 0:
            startingNodeName = data[0] # the starting node is the first letter found
            # search for startingNode inside the list of the nodes we know
            startingNode = FindNodeByName(startingNodeName.strip(), listOfTotalNodes)
            if startingNode is not "":
                # if startingNode was not found in the list, create a new node and add it to list
                if startingNode is None:
                    startingNode = Node(startingNodeName.strip())
                    #print ("New node created: " + startingNodeName.strip())  
                    listOfTotalNodes.append(startingNode)
                    #print("Node: " + startingNode.name + ", added to list")
        if len(data) > 1: # if the line contains an ending node
            endingNodeName = data[1] # the ending node is the second letter found
            #print ("\n--New line: " + startingNodeName +", "+ endingNodeName)
            # if starting node is the same with ending node return the list as it was (for our case a node can not make a transition to itself)
            if startingNodeName == endingNodeName:
                return listOfTotalNodes
            # search for endingNode inside the list of the nodes we know
            endingNode = FindNodeByName(endingNodeName.strip(), listOfTotalNodes)
            # if endingNode was not found in the list, create a new node and add it to list
            if (endingNode is not ""):
                if endingNode is None:
                    endingNode = Node(endingNodeName.strip())
                    #print ("New node created: " + endingNodeName)
                    listOfTotalNodes.append(endingNode)
                    #print("Node: " + endingNode.name + ", added to list")
                # if endingNode not in startingNode's neighbours, add it
                if endingNode not in startingNode.neighbours:
                    #print("New neighbour: " + endingNode.name + ", added to node: " + startingNode.name)
                    startingNode.neighbours.append(endingNode)
                # if startingNode not in endingNode's neighbours, add it
                if startingNode not in endingNode.neighbours:
                    endingNode.neighbours.append(startingNode)
                    #print("neighbour: " + startingNode.name + " added to node: " + endingNode.name)

    # return the list with the new nodes and transitions added (if were any)
    return listOfTotalNodes

# Searches if there is a known node with the same name and if true returns it. 
def FindNodeByName(name, listOfTotalNodes):
	for x in listOfTotalNodes:
		if x.name == name:	
			return x
	#print ("Node: " + name + ", not found")
	return None

def FindNodesDegree (listOfTotalNodes):  
    # create a dictionary with nodes as keys and numbers as value. Here we will store the final results
    nodesAndDegree = {}
    queue = MyPriorityQueue();
    # at this loop, we initialize the queue. each node will get a priority equal to the number of neighbours
    for node in listOfTotalNodes:
        queue.addElement(node)  
    # while there are nodes that have not been checked
    while (queue.getQueueLength() > 0):       
        node = queue.takeElementWithLowestK() # get the node with the smallest number of neighbours from queue
        #print ("node: " + node.name + " degree set to: " + str(len(node.neighbours)))
        nodesAndDegree.update({node:len(node.neighbours)}) # update the dictionary that stores the results
        # for each of this node neighbours remove this node
        for neighbour in node.neighbours:
            if len(neighbour.neighbours) > len(node.neighbours): # though only if the number of total of the neighbour's neighbours is bigger than current K
                neighbour.neighbours.remove(node) # remove the node from it's neighbours                       
                #print ("Node: " + node.name + " removed from Neighbour: " + neighbour.name)
                queue.rearrange(neighbour) # re-arrange this node in the queue depending on it's new degree number
                #print ("Node: " + neighbour.name + " has now K: " + str(len(neighbour.neighbours)))	
    return nodesAndDegree



totalNodes = []
text = []
if (len(sys.argv) > 1):
    path = sys.argv[1]
else:
    print("Write the full path of the file that contains the graph")
    path = input("")
    print("you typed: "+ path)

text = MyOpenFile(path, text)
print("Opened file succesfully")

if (text is not None):
    for line in text:
        #print(line)
        totalNodes = createGraphFromText(line, totalNodes)
    #print("\n-----List of all nodes-----")
    #for node in totalNodes:
    #    print("\nNode: " + node.name)
    #    print ("available transitions:")
    #    for neighbour in node.neighbours:
    #        print ("neighbour: " + neighbour.name)
    print("Calculatin results, please wait...")
    nodesAndDegree = dict(FindNodesDegree(totalNodes))
    print("\n\n----RESULTS:-----")
    for k in range(0, len(nodesAndDegree)):
        print ("Node: " + FindNodeByName(str(k), nodesAndDegree).name + " has core: " + str(nodesAndDegree[FindNodeByName(str(k), nodesAndDegree)]))
else:
    print ("An error occured while opening the the file. Please re-open the program and try again")

