import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import tkinter as tk
import random
import time
import math

matplotlib.use('TkAgg')
visited = {}
graph = nx.Graph()

def OneCharDiff(string1, string2):
    # return True if strings differ by one character
    # return False otherwise pass
    if string1 == string2:
        return False
    if len(string1) != len(string2):
        return False
    else:
    	# length is the same and the strings aren't the same
        count_diffs = 0
        for a, b in zip(string1, string2):
            # zip pairs the values in the same position of the two strings -> 0,0 - 1,1 - 2,2 -...
            if a != b:
                if count_diffs:
                    # if you enter here it means it's the second time you found a mismatch
                    return False
                count_diffs += 1
        return True

def AddRemoveOneCharDiff(string1, string2):
    # return True if strings differ by one character added or removed
    # return False otherwise pass
    if abs(len(string1) - len(string2)) != 1:
        return False
    if len(string1) < len(string2):
        string1, string2 = string2, string1
    it1 = iter(string1)
    it2 = iter(string2)
    # itn contains a character of the string and can be iterated upon with the method next
    count_diffs = 0
    c1 = next(it1, None)
    c2 = next(it2, None)
    while True:
        if c1 != c2:
            if count_diffs: return False
            count_diffs = 1
            try:
                c1 = next(it1)
            except StopIteration:
                return True
        else:
            try:
                c1 = next(it1)
                c2 = next(it2)
            except StopIteration:
                return True

def Anagram(string1, string2):
    # return True if strings are anagrams
    # return False otherwise pass
    # we can sort the letters of two strings in alphabetical order and see if they're the same
    # cinema,nemica -> aceimn,aceimn -> equal -> anagrams
    return sorted(string1) == sorted(string2)
    
def createMiniGraphWrapper(dictionary, source, destination, iterations):
    # wrapper method that adds the source to the visited list, adds source and destination to the dictionary
    # if not already present, sets up the visited dictionary and starts the recursive calls
    # returns a graph containing all the nodes we explored
    G = nx.Graph()
    added = [source]
    # the first time we call the recursive method we start from the source node only
    G.add_node(source)
    G.add_node(destination)
    # we add source and destination to the graph so that even if we don't find any edge we're still able
    # to print the two core nodes
    
    if len(source) > len(dictionary):
        dictionary.setdefault(len(source),[])
        dictionary[len(source)].append(source)
    if len(destination) > len(dictionary):
        if len(source) != len(destination):
            dictionary.setdefault(len(destination),[])
        dictionary[len(destination)].append(destination)
    # we need to make sure source and destination are added to the dictionary, so that we can proceed to
    # a seamless exploration phase during recursive calls. Additional checks to be made when adding the
    # destination to make sure we don't lose the source node, which is added first
    
    for l in dictionary.keys():
        for node in dictionary[l]:
            visited.setdefault(node,0)
            # now that all nodes are in the dictionary, we can set up the visited dictionary properly
            # this is mostly needed during the first run, but if we call the method with words that
            # don't exist yet we need to set their value to 0
    
    return createMinGraphRecursive(G, dictionary, added, destination, len(source), iterations)
    
def createMinGraphRecursive(G, dictionary, added, destination, length, iteration):
    # method that does most of the work in terms of finding the minimum necessary graph
    # i counts the number of steps we want to take / distance at most starting from the source node
    
    if length not in dictionary.keys() or iteration == 0:
        # base recursive step - we stop exploring if there's no word on this level or we're out of steps
        return G;
        
    addedLeft = []
    addedMid = []
    addedRight = []
    # every time we find new nodes during an exploration step, we add them to the dedicated list.
    # we separate them into different lists depending on where we find them - lower, same or higher length

    # EXPLORATION PHASE
    # could be made better by creating a second dictionary from which to remove the words we have visited
    for node in added:
        # start from the set of nodes we are given - this will contain only the source node the first time
        visited[node] = iteration  
        # set the node we are starting from as visited - we won't be visiting these nodes again unless their
        # value is too low compared to the one we are currently looking at - this allows for exploration
        # when starting from an already existing graph and reducing the number of nodes we have to revisit
        for node2 in dictionary[length]:
            # first we check for other nodes with the same length as the words we are currently observing
            # sometimes we are exploring a set of words coming from a different length, but there could be
            # an anagram or a word with 1 char difference here
            if OneCharDiff(node, node2):
                G.add_edge(node, node2, weight=10)
                if(visited[node2] < iteration - 1):
                    # we use iteration - 1 to cut down unnecessary visits to nodes
                    addedMid.append(node2)
            elif Anagram(node, node2) and node != node2:
                G.add_edge(node, node2, weight=30)
                if(visited[node2] < iteration - 1):
                    addedMid.append(node2)
        if len(node) - 1 in dictionary.keys():
            for node2 in dictionary[length - 1]:
                # then we look for words in a level with lower length. We could look in higher length first,
                # it doesn't really matter. This time we don't look for anagrams and 1 char difference but
                # for a removed or added character instead, because we're on different lengths
                if AddRemoveOneCharDiff(node, node2):
                    G.add_edge(node, node2, weight=20)
                    if(visited[node2] < iteration - 1):
                        addedLeft.append(node2)
        if len(node) + 1 in dictionary.keys():
            for node2 in dictionary[length + 1]:
                # looking for words in a level with higher length
                if AddRemoveOneCharDiff(node, node2):
                    G.add_edge(node, node2, weight=20)
                    if(visited[node2] < iteration - 1):
                        addedRight.append(node2)
    
    G.add_edges_from(createMinGraphRecursive(G, dictionary, addedLeft, destination, length - 1, iteration - 1).edges())
    G.add_edges_from(createMinGraphRecursive(G, dictionary, addedMid, destination, length, iteration - 1).edges())
    G.add_edges_from(createMinGraphRecursive(G, dictionary, addedRight, destination, length + 1, iteration - 1).edges())
    # triple recursive call to explore in different directions - lower length, same length, higher length
    # starting from the new nodes we just found but separated as discussed earlier
    
    return G
    
def printWordsLen(dictionary):
    for l in dictionary.keys():
        print("Number of words with length " + str(l) + " --> " + str(len(dictionary[l])))

def startGraph(dictionary):
    # method that gets values from Entries, starts the wrapper method and prints stuff on screen
    plt.clf()
    # clean the graph window in case there was something before
    
    source = sourceValue.get()
    if(len(source) == 0):
        # if nothing is written in the source entry, use a random word from the dictionary
        keys = list(dictionary.keys())
        source = random.choice(dictionary[random.choice(keys)])
        keys=[]

    dest = destValue.get()
    if(len(dest) == 0):
        # if nothing is written in the destination entry, use a random word from the dictionary
        keys = list(dictionary.keys())
        while True:
            # here make sure it's different from the source if random
            dest = random.choice(dictionary[random.choice(keys)])
            if(source != dest): break
        keys=[]
        
    steps = int(stepsValue["text"])
    print("Source -> " + source)
    print("Dest -> " + dest)
    print("Maximum distance -> " + str(steps))
    graph.add_node(source)
    graph.add_node(dest)
    # we try to add source and dest right away in order to check if the path already exists, so we can
    # sometimes cut down on unnecessary work
    
    if nx.has_path(graph,source,dest) == False:
        start = time.time()
        graph.add_edges_from(createMiniGraphWrapper(dictionary, source, dest, math.ceil(steps/2)).edges())
        graph.add_edges_from(createMiniGraphWrapper(dictionary, dest, source, math.floor(steps/2)).edges())
        # we introduced bidirectional exploration to reduce the overall number of nodes
        # in case of an odd number of steps needed, the first call does one additional step
        end = time.time()
        print("Time taken to create the graph -> " + str(end - start))
        # better check how long the method runs for   

    print("There are " + str(len(graph.nodes())) + " nodes in the graph")
    
    if nx.has_path(graph,source,dest) == True and nx.shortest_path_length(graph,source,dest) <= steps:
        # if there's a path from source to dest we print that + those nodes' neighbors
        path = []
        extendedPath = []
        path = nx.shortest_path(graph,source,dest)
        print("There is a path from " + source + " to " + dest)
        for node in path:
            print(str(node))
            for neighbor in nx.neighbors(graph,node):
                extendedPath.append(neighbor)
        smallG = nx.subgraph(graph,extendedPath)
        #smallG = nx.subgraph(graph,path)  
        # use this instead of the one above if you want to see the path without neighbors
        node_colors = ["green" if n in path and n != source and n != dest else "yellow" if n == source or n == dest else "red" for n in smallG.nodes()]
        nx.draw_networkx(smallG, node_color=node_colors)
    else:
        # currently we print the whole subgraph if no path is found. This may lead to errors if too many nodes are present
        # download (pip) scipy to fix full graph visualization
        print("There's no path from " + source + " to " + dest + " in only " + str(steps) + " steps")
        node_colors = ["blue" if n == source else "red" if n == dest else "gray" for n in graph.nodes()]
        nx.draw_networkx(graph, node_color=node_colors)
        
    plt.savefig("graph.png")
    # save the graph to an image because we can
    plt.show()


def increase():
    # increase the value of label with number of steps
    value = int(stepsValue["text"])
    stepsValue["text"] = f"{value + 1}"

def decrease():
    # decrease the value of label with number of steps
    value = int(stepsValue["text"])
    if(value > 1):
        stepsValue["text"] = f"{value - 1}"

if __name__=="__main__":
    dictionary = {}
    # setting up a dictionary of lists of words, with key = length of word

    with open('./words.italian.txt') as f:
        # add nodes from words.italian.txt -- or littledictionary.txt for testing
        for line in f:
            if(len(line.strip()) > 0):
                # ignoring empty strings because they're useless
                if len(line.strip()) not in dictionary.keys():
                    dictionary.setdefault(len(line.strip()),[])
                    # the first time a new length is found initialize an empty list 
                dictionary[len(line.strip())].append(line.strip())

    # printWordsLen(dictionary)
    # print number of words in the dictionary for various lengths
    
    window = tk.Tk()
    window.title("Progetto IUM - Python")
    window.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7] , minsize=40, weight=1)
    window.columnconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8], minsize=50, weight=1)
    
    mainLabel = tk.Label(
        text="Insert two words and the maximum number of steps",
        width=25,
        height=5)
    mainLabel.grid(row=0, column=0, sticky="nsew", columnspan=9)
    
    sourceLabel = tk.Label(text="Source word")
    destLabel = tk.Label(text="Destination word")
    sourceValue = tk.Entry(width=30)
    destValue = tk.Entry(width=30)
    
    sourceLabel.grid(row=1, column=0, sticky="nsew", columnspan=9)
    sourceValue.grid(row=2, column=3, sticky="nsew", columnspan=3)
    destLabel.grid(row=3, column=0, sticky="nsew", columnspan=9)
    destValue.grid(row=4, column=3, sticky="nsew", columnspan=3)
    
    stepsLabel = tk.Label(text="Maximum number of steps")
    stepsDecrease = tk.Button(text="-", command=decrease)
    stepsValue = tk.Label(text="1")
    stepsIncrease = tk.Button(text="+", command=increase)
    
    stepsLabel.grid(row=5, column=3, sticky="nsew", columnspan=3)
    stepsDecrease.grid(row=6, column=3, sticky="nsew")
    stepsValue.grid(row=6, column=4)
    stepsIncrease.grid(row=6, column=5, sticky="nsew")
    
    findButton = tk.Button(
        # this button starts the search method
        text="FIND PATH",
        width=25,
        height=5,
        fg="black",
        command=lambda: startGraph(dictionary)
        )
    findButton.grid(row=7, column=1, sticky="nsew", columnspan=3)
        
    findButton = tk.Button(
        # this button starts the search method
        text="RESET GRAPH",
        width=25,
        height=5,
        fg="black",
        command=lambda: startGraph(dictionary)
        )
    findButton.grid(row=7, column=5, sticky="nsew", columnspan=3)
    window.mainloop()

