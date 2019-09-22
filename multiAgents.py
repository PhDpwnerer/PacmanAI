# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

def manhattanDistance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2-x1)+abs(y2-y1)

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        foodLeft = newFood.count()



        currentScore = successorGameState.getScore()
        result = currentScore

        for x in range(len(newFood.data)):
            for y in range(len(newFood[x])):
                if (newFood[x][y]):
                    result += 1/(manhattanDistance(newPos, (x,y))*foodLeft) #closer the food, the better
        for i in range(len(newGhostStates)):
            distanceToGhost = manhattanDistance(newPos, newGhostStates[i].getPosition())
            if newScaredTimes[i] == 0:
                if distanceToGhost > 0:
                    result -= 1/distanceToGhost #further the ghosts, the better
                else:
                    result = -100 #don't let the ghost touch you!
            else:
                result += (5/distanceToGhost)*(newScaredTimes[i]/10) #while you can eat ghosts, having them close to you is not a bad thing

        return result

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent & AlphaBetaPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 7)
    """

    def value(self, gameState, player, depth, numAgents):
        if gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)

        if player == 0:
            depth = depth+1
            if depth > self.depth:
                val = self.evaluationFunction(gameState)
                #print(val)
                return val
            actions = gameState.getLegalActions(0)
            bestValue = -100000
            for action in actions:
                tempVal = self.value(gameState.generateSuccessor(0, action), 1, depth, numAgents)
                if tempVal > bestValue:
                    bestValue = tempVal
        if player > 0:
            actions = gameState.getLegalActions(player)
            bestValue = 100000
            for action in actions:
                tempVal = self.value(gameState.generateSuccessor(player, action), (player+1)%(numAgents), depth, numAgents)
                if tempVal < bestValue:
                    bestValue = tempVal
        return bestValue

        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game
        """

    def getAction(self, gameState):

        actions = gameState.getLegalActions(0)
        numAgents = gameState.getNumAgents()
        bestValue = -100000
        bestAction = Directions.STOP
        for action in actions:
            tempVal = self.value(gameState.generateSuccessor(0, action), 1, 1, numAgents)
            if tempVal > bestValue:
                bestValue = tempVal
                bestAction = action
        return bestAction


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 8)
    """
    def value(self, gameState, player, depth, numAgents):
        if gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)

        if player == 0:
            depth = depth+1
            if depth > self.depth:
                val = self.evaluationFunction(gameState)
                #print(val)
                return val
            actions = gameState.getLegalActions(0)
            bestValue = -100000
            for action in actions:
                tempVal = self.value(gameState.generateSuccessor(0, action), 1, depth, numAgents)
                if tempVal > bestValue:
                    bestValue = tempVal
        if player > 0:
            actions = gameState.getLegalActions(player)
            bestValue = 0
            for action in actions:
                tempVal = self.value(gameState.generateSuccessor(player, action), (player+1)%(numAgents), depth, numAgents)
                bestValue += tempVal
            bestValue = bestValue/len(actions)
        return bestValue

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        actions = gameState.getLegalActions(0)
        numAgents = gameState.getNumAgents()
        bestValue = -100000
        bestAction = Directions.STOP
        for action in actions:
            tempVal = self.value(gameState.generateSuccessor(0, action), 1, 1, numAgents)
            if tempVal > bestValue:
                bestValue = tempVal
                bestAction = action
        return bestAction

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 9).

    DESCRIPTION: <write something here so we know what you did>
    """
    newPos = currentGameState.getPacmanPosition()
    
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    newFood = currentGameState.getFood()
    
    foodLeft = newFood.count()



    currentScore = currentGameState.getScore()
    result = currentScore

    for x in range(len(newFood.data)):
        for y in range(len(newFood[x])):
            if (newFood[x][y]):
                result += 1/(manhattanDistance(newPos, (x,y))*foodLeft) #closer the food, the better
    for i in range(len(newGhostStates)):
        distanceToGhost = manhattanDistance(newPos, newGhostStates[i].getPosition())
        if newScaredTimes[i] == 0:
            if distanceToGhost > 0:
                result -= 1/distanceToGhost #further the ghosts, the better
            else:
                result = -100 #don't let the ghost touch you!
        else:
            result += (5/distanceToGhost)*(newScaredTimes[i]/10) #while you can eat ghosts, having them close to you is not a bad thing

    return result

# Abbreviation
better = betterEvaluationFunction

