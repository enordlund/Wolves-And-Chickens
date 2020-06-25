#!/usr/bin/python

from collections import namedtuple
import math
import sys

# defining data types
BankState = namedtuple("BankState", "chickens wolves boat")

EnvironmentState = namedtuple("EnvironmentState", "leftBankState rightBankState")

Node = namedtuple("Node", "state successorNodes parentNode depth aStarCost")

initialState = None
goalState = None

currentNode = None

nodeExpansions = 0

# function for parsing initial state from file
# 	State files are formatted as follows:
#		0,0,0
#		3,3,1
#	Each line is structured as: "chickens, wolves, boats"
#	The first line is the left bank.
#	The second line is the right bank.
def parseStateFiles():
	# preparing to store structs in the global variables.
	global initialState
	global goalState
	
	# file names are passed as arguments
	initialStateFilePath = sys.argv[1]
	goalStateFilePath = sys.argv[2]
	
	
	# trying initial state first
	initialStateFile = open(initialStateFilePath)
	
	# first line is left bank
	initialLeftBankStateArray = initialStateFile.readline().split(",")
	
	# second line is right bank
	initialRightBankStateArray = initialStateFile.readline().split(",")
	
	
	# create initial state tuple
	
	initialLeftBankState = BankState(int(initialLeftBankStateArray[0]), int(initialLeftBankStateArray[1]), int(initialLeftBankStateArray[2]))
	
	initialRightBankState = BankState(int(initialRightBankStateArray[0]), int(initialRightBankStateArray[1]), int(initialRightBankStateArray[2]))
	
	initialState = EnvironmentState(initialLeftBankState, initialRightBankState)
	
	# at this point, the initial state should be stored in the global variable.
	
	
	
	# trying goal state
	goalStateFile = open(goalStateFilePath)
	
	# left bank line
	goalLeftBankStateArray = goalStateFile.readline().split(",")
	
	# right bank line
	goalRightBankStateArray = goalStateFile.readline().split(",")
	
	# creating goal state tuple
	goalLeftBankState = BankState(int(goalLeftBankStateArray[0]), int(goalLeftBankStateArray[1]), int(goalLeftBankStateArray[2]))
	
	goalRightBankState = BankState(int(goalRightBankStateArray[0]), int(goalRightBankStateArray[1]), int(goalRightBankStateArray[2]))
	
	goalState = EnvironmentState(goalLeftBankState, goalRightBankState)
	
	# at this point, both the initial and goal states should be stored in their global variables.
	
	return








# function for determining successors of a node
#	Successor states are inspected in the following order:
	# 1) Put one chicken in the boat
	# 2) Put two chickens in the boat
	# 3) Put one wolf in the boat
	# 4) Put one wolf and one chicken in the boat
	# 5) Put two wolves in the boat
def getSuccessorNodes(forNode):
	# this array will be added to the node after it is populated.
	successorNodes = []
	
	boatBank = None
	nextBank = None
	
	boatBankIsLeftBank = False
	
	# determine which bank has the boat
	if forNode.state.leftBankState.boat == 1:
		# the boat is on the left bank
		boatBank = forNode.state.leftBankState
		nextBank = forNode.state.rightBankState
		boatBankIsLeftBank = True
	else:
		# the boat is on the right bank
		boatBank = forNode.state.rightBankState
		nextBank = forNode.state.leftBankState
	
	
	# Now, analyze potential successor states.
	
	# next states will have animals moved from the boat bank to the next bank.
	
	# For the first case (moving one chicken from current to next):
		# The boat bank must have at least one chicken.
		# The boat bank must have more chickens than wolves.
			# (If chickens <= wolves, moving one will violate rules)
			# OR (chickens == 1) for the case of leaving wolves with no chickens
		# Next bank must meet: (wolves - chickens) <= 1.
	if (boatBank.chickens >= 1) and ((boatBank.chickens > boatBank.wolves) or (boatBank.chickens == 1)) and ((nextBank.wolves - nextBank.chickens) <= 1):
		tempBoatBankState = BankState(boatBank.chickens - 1, boatBank.wolves, 0)
		
		tempNextBankState = BankState(nextBank.chickens + 1, nextBank.wolves, 1)
		
		if boatBankIsLeftBank:
			successorState = EnvironmentState(tempBoatBankState, tempNextBankState)
			
			tempNode = Node(successorState, None, forNode, forNode.depth + 1, None)
			tempNode = aStarEvaluatedNode(tempNode)
			
			# adding successor to the array
			successorNodes.append(tempNode)
		else:
			successorState = EnvironmentState(tempNextBankState, tempBoatBankState)
			
			tempNode = Node(successorState, None, forNode, forNode.depth + 1, None)
			tempNode = aStarEvaluatedNode(tempNode)
			
			# adding successor to the array
			successorNodes.append(tempNode)
	
	# For the second case (moving two chickens from current to next):
		# The boat bank must have at least two chickens.
		# The boat bank must have at least two more chickens than wolves (chickens > (wolves + 1)), or (chickens == 2)
		# Next bank must meet: (wolves - chickens) <= 2.
	if (boatBank.chickens >= 2) and ((boatBank.chickens > (boatBank.wolves + 1)) or (boatBank.chickens == 2)) and ((nextBank.wolves - nextBank.chickens) <= 2):
		tempBoatBankState = BankState(boatBank.chickens - 2, boatBank.wolves, 0)
		
		tempNextBankState = BankState(nextBank.chickens + 2, nextBank.wolves, 1)
		
		if boatBankIsLeftBank:
			successorState = EnvironmentState(tempBoatBankState, tempNextBankState)
			
			tempNode = Node(successorState, None, forNode, forNode.depth + 1, None)
			tempNode = aStarEvaluatedNode(tempNode)
			
			# adding successor to the array
			successorNodes.append(tempNode)
		else:
			successorState = EnvironmentState(tempNextBankState, tempBoatBankState)
			
			tempNode = Node(successorState, None, forNode, forNode.depth + 1, None)
			tempNode = aStarEvaluatedNode(tempNode)
			
			# adding successor to the array
			successorNodes.append(tempNode)
		
	
	# For the third case (moving one wolf from current to next):
		# Next bank must have more chickens than wolves, or no chickens
		# Boat bank must meet: (wolves >= 1)
		# (chickens <= wolves guaranteed for boat bank)
	if ((nextBank.chickens == 0) or (nextBank.chickens > nextBank.wolves)) and (boatBank.wolves >= 1):
		tempBoatBankState = BankState(boatBank.chickens, boatBank.wolves - 1, 0)
		
		tempNextBankState = BankState(nextBank.chickens, nextBank.wolves + 1, 1)
		
		if boatBankIsLeftBank:
			successorState = EnvironmentState(tempBoatBankState, tempNextBankState)
			
			tempNode = Node(successorState, None, forNode, forNode.depth + 1, None)
			tempNode = aStarEvaluatedNode(tempNode)
			
			# adding successor to the array
			successorNodes.append(tempNode)
		else:
			successorState = EnvironmentState(tempNextBankState, tempBoatBankState)
			
			tempNode = Node(successorState, None, forNode, forNode.depth + 1, None)
			tempNode = aStarEvaluatedNode(tempNode)
			
			# adding successor to the array
			successorNodes.append(tempNode)
			
	# For the fourth case (moving one wolf and one chicken from current to next):
		# Next bank must meet: wolves <= chickens
			# this addresses the case where it could have wolves with no chickens as well.
		# Boat bank must meet: (wolves >= 1) and (chickens >= 1)
	if (nextBank.wolves <= nextBank.chickens) and (boatBank.wolves >= 1) and (boatBank.chickens >= 1):
		tempBoatBankState = BankState(boatBank.chickens - 1, boatBank.wolves - 1, 0)
		
		tempNextBankState = BankState(nextBank.chickens + 1, nextBank.wolves + 1, 1)
		
		if boatBankIsLeftBank:
			successorState = EnvironmentState(tempBoatBankState, tempNextBankState)
			
			tempNode = Node(successorState, None, forNode, forNode.depth + 1, None)
			tempNode = aStarEvaluatedNode(tempNode)
			
			# adding successor to the array
			successorNodes.append(tempNode)
		else:
			successorState = EnvironmentState(tempNextBankState, tempBoatBankState)
			
			tempNode = Node(successorState, None, forNode, forNode.depth + 1, None)
			tempNode = aStarEvaluatedNode(tempNode)
			
			# adding successor to the array
			successorNodes.append(tempNode)
	
	# For the fifth case (moving two wolves from current to next):
		# Next bank must meet: (wolves <= (chickens - 1)) or chickens == 0
		# Boat bank must meet: (wolves >= 2)
	if ((nextBank.wolves <= (nextBank.chickens - 1)) or (nextBank.chickens == 0)) and (boatBank.wolves >= 2):
		tempBoatBankState = BankState(boatBank.chickens, boatBank.wolves - 2, 0)
		
		tempNextBankState = BankState(nextBank.chickens, nextBank.wolves + 2, 1)
		
		if boatBankIsLeftBank:
			successorState = EnvironmentState(tempBoatBankState, tempNextBankState)
			
			tempNode = Node(successorState, None, forNode, forNode.depth + 1, None)
			tempNode = aStarEvaluatedNode(tempNode)
			
			# adding successor to the array
			successorNodes.append(tempNode)
		else:
			successorState = EnvironmentState(tempNextBankState, tempBoatBankState)
			
			tempNode = Node(successorState, None, forNode, forNode.depth + 1, None)
			tempNode = aStarEvaluatedNode(tempNode)
			
			# adding successor to the array
			successorNodes.append(tempNode)
			
	
	# Next, return the successors
#	print(successorNodes)
	return successorNodes





# function to apply successor nodes to a Node object
# returns the node with successors
def expand(node):
	global nodeExpansions
	tempSuccessorNodes = getSuccessorNodes(node)
	tempNode = Node(node.state, tempSuccessorNodes, node.parentNode, node.depth + 1, None)
	tempNode = aStarEvaluatedNode(tempNode)
	nodeExpansions += 1
	return tempNode


# function for printing file parsing results
def printParsedStates():
	print("initialState:")
	print(initialState)
	
	print("goalState:")
	print(goalState)










# function for running Breadth-First Search
	# It is assumed that the initial and goal state files have been successfully parsed before calling this function.
def runBFS():
	print("Running BFS mode...")
	
	global currentNode
	
	# first, initialize the root node with initial state
	currentNode = Node(initialState, None, None, 0, None)
	
	# establish a node queue with the initial state root node
	nodeQueue = [currentNode]
	
	
	checkedStates = []
	
	while len(nodeQueue) > 0:
		if currentNode.state == goalState:
			# the current node was assigned in the else section of this loop, or the initial state is the goal state.
			break
		else:
			# popping a node from the queue for inspection
			node = nodeQueue.pop(0)
			# the node is not the goal, so inspect its successors
			node = expand(node)
			for successor in node.successorNodes:
				if successor.state == goalState:
					# we have found the goal state, so stop looping
					currentNode = successor
					break
				else:
					# the successor is not the goal, so add it to the queue for expansion.
					if successor.state not in checkedStates:
						# placing non-duplicate successor at end of queue for bfs
						nodeQueue.append(successor)
						checkedStates.append(successor.state)
	
	
	# at this point, currentNode is either the goal, or the goal was not found.
	
	return






# function for running depth-first search
	# It is assumed that the initial and goal state files have been successfully parsed before calling this function.
def runDFS():
	print("Running DFS mode...")
	
	global currentNode
	# first, initialize the root node with initial state
	currentNode = Node(initialState, None, None, 0, None)
	
	# establish a node queue with the initial state root node
	nodeQueue = [currentNode]
	
	
	checkedStates = []
	
	while len(nodeQueue) > 0:
		if currentNode.state == goalState:
			# the current node was assigned in the else section of this loop, or the initial state is the goal state.
			break
		else:
			# popping a node from the queue for inspection
			node = nodeQueue.pop(0)
			# the node is not the goal, so inspect its successors
			node = expand(node)
			for successor in node.successorNodes:
				if successor.state == goalState:
					# we have found the goal state, so stop looping
					currentNode = successor
					break
				else:
					# the successor is not the goal, so add it to the queue for expansion.
					if successor.state not in checkedStates:
						# placing non-duplicate successor at front of queue for dfs
						nodeQueue.insert(0, successor)
						checkedStates.append(successor.state)
	
	
	# at this point, currentNode is either the goal, or the goal was not found.
	
	return





# modified runDFS() for depth limit, in support of runIDDFS()
def runDepthLimitedDFS(withDepthLimit):
#	print("runDepthLimitedDFS(withDepthLimit: " + str(withDepthLimit) + ")")
	
	global currentNode
	# first, initialize the root node with initial state
	currentNode = Node(initialState, None, None, 0, None)
	
	# establish a node queue with the initial state root node
	nodeQueue = [currentNode]
	
	
	checkedStates = []
	
	while len(nodeQueue) > 0:
		if currentNode.state == goalState:
			# the current node was assigned in the else section of this loop, or the initial state is the goal state.
			break
		else:
			# popping a node from the queue for inspection
			node = nodeQueue.pop(0)
			# the node is not the goal, so inspect its successors
			node = expand(node)
			for successor in node.successorNodes:
				if successor.state == goalState:
					# we have found the goal state, so stop looping
					currentNode = successor
					break
				else:
					# the successor is not the goal, so add it to the queue for expansion.
					# because this is depth-limited, the successor depth must be less than the limit to be added to the queue.
					if (successor.state not in checkedStates) and (successor.depth < withDepthLimit):
						# placing non-duplicate successor at front of queue for dfs
						nodeQueue.insert(0, successor)
						checkedStates.append(successor.state)
	
	
	# at this point, currentNode is either the goal, or the goal was not found.
	
	return





# function for iterative deepening depth-first search
def runIDDFS():
	print("Running IDDFS mode...")
	
	global currentNode
	
	currentNode = Node(initialState, None, None, 0, None)
	
	depthLimitIterator = 1 # starting at 1, because 0 case is handled by the if statement in the while loop of runDepthLimitedDFS()
	
	while currentNode.state != goalState:
		runDepthLimitedDFS(depthLimitIterator)
		depthLimitIterator += 1
	
	return






# supporting path cost function for A-Star evaluation function
	# written assuming all path costs are 1, aka node path cost = node depth
def g(node):
	return node.depth
	
	
# supporting heuristic function for A-Star evaluation function
	# heuristic function estimates remaining path cost by:
		# summing difference between state values of left bank, and goal values of left bank
		# dividing that sum by two to account for the ability to transport two animals at once
def h(node):
	remainingEstimate = 0
	
	remainingEstimate += abs(node.state.leftBankState.chickens - goalState.leftBankState.chickens)
	
	remainingEstimate += abs(node.state.leftBankState.wolves - goalState.leftBankState.wolves)
	
	#remainingEstimate += abs(node.state.leftBankState.boat - goalState.leftBankState.boat)
	
	return remainingEstimate / 2


def aStarEvaluatedNode(node):
	evaluation = g(node) + h(node)
	tempNode = Node(node.state, node.successorNodes, node.parentNode, node.depth, evaluation)
	return tempNode

# function for running A-Star search
def runAStar():
	print("Running A-Star mode...")
	
	global currentNode
	
	# first, initialize the root node with initial state
	currentNode = Node(initialState, None, None, 0, None)
	currentNode = aStarEvaluatedNode(currentNode)
	
	# establish a node queue with the initial state root node
	nodeQueue = [currentNode]
	
	
	checkedStates = []
	
	while len(nodeQueue) > 0:
		if currentNode.state == goalState:
			# the current node was assigned in the else section of this loop, or the initial state is the goal state.
			break
		else:
			# popping a node from the queue for inspection
			node = nodeQueue.pop(0)
			# the node is not the goal, so inspect its successors
			node = expand(node)
			for successor in node.successorNodes:
				if successor.state == goalState:
					# we have found the goal state, so stop looping
					currentNode = successor
					break
				else:
					# the successor is not the goal, so add it to the queue for expansion.
					if successor.state not in checkedStates:
						# placing non-duplicate successor at end of queue for bfs
						nodeQueue.append(successor)
						
						# now sort the queue according to its evaluated cost (increasing)
						nodeQueue.sort(key=lambda elem: elem[4])
						
						checkedStates.append(successor.state)
	
	
	# at this point, currentNode is either the goal, or the goal was not found.
	
	return






# function for describing a bank state
def bankStateDescription(forBankState):
	descriptionBuffer= ""
	
	descriptionBuffer += str(forBankState.chickens)
	
	if forBankState.chickens == 1:
		descriptionBuffer += " chicken, and "
	else:
		descriptionBuffer += " chickens, and "
	
	descriptionBuffer += str(forBankState.wolves)
	
	if forBankState.wolves == 1:
		descriptionBuffer += " wolf"
	else:
		descriptionBuffer += " wolves"
	
	if forBankState.boat == 1:
		descriptionBuffer += " (with boat)."
	else:
		descriptionBuffer += "."
	
	return descriptionBuffer


# function for appending to the user-defined output file
def appendToOutputFile(string):
	file = open(sys.argv[4], "a")
	file.write(string)
	file.close()


# function for overwriting to the output file
def overwriteToOutputFile(string):
	file = open(sys.argv[4], "w")
	file.write(string)
	file.close()


def writeOutcome():
	
	outcomeBuffer = ""
	
	# print the number of nodes expanded
	outcomeBuffer = "Nodes expanded: " + str(nodeExpansions) + "\n\n"
	
	global currentNode
	
	
	
	if currentNode.state == goalState:
		# the goal state was achieved with the current node
		# backtrace the path for output
		solutionPath = []
		while currentNode.parentNode != None:
			solutionPath.insert(0, currentNode.state)
			currentNode = currentNode.parentNode
		
		# insert the root node
		solutionPath.insert(0, currentNode.state)
		
		outcomeBuffer += "Nodes in solution: " + str(len(solutionPath)) + "\n\n"
		
		# print the solution
		outcomeBuffer += "Solution (starting from initial state):\n\n"
		for state in solutionPath:
			leftBankDescriptor = "Left Bank: " + bankStateDescription(state.leftBankState) + "\n"
			rightBankDescriptor = "Right Bank: " + bankStateDescription(state.rightBankState) + "\n"
			
			outcomeBuffer += leftBankDescriptor + rightBankDescriptor + "\n"
		
		print()
		print(outcomeBuffer)
		overwriteToOutputFile(outcomeBuffer)
		print("The outcome was written to \"" + sys.argv[4] + "\".")
	else:
		# the goal state was not found.
		print("The goal state was not found.")










def run():
	parseStateFiles()
#	printParsedStates()
	
	mode = sys.argv[3]
	
	if mode == "bfs":
		runBFS()
	elif mode == "dfs":
		runDFS()
	elif mode == "iddfs":
		runIDDFS()
	elif mode == "astar":
		runAStar()
	else:
		print("ERROR: Unknown mode, \"" + mode + "\"")
	
	writeOutcome()
	
	print("Done.")


run()
