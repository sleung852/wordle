from wordle import Wordle
from agents import SimpleAgent, HeuristicAgent
# from collections import deque
from tqdm import tqdm
import multiprocessing

def runMaxGuessChain(n=4):
    assert n > 0, "No. of processes cannot be 0 or negative"
    game = Wordle()
    wordChoices = game.WORDLIST
    if n == 1:
        return worker(0, wordChoices)
    split = int(len(wordChoices) / n)
    wordChoicesList = []
    
    for p in range(n-1):
        wordChoicesList.append(wordChoices[p*split:(p+1)*split])
    wordChoicesList.append(wordChoices[(p+1)*split:])

    pool = multiprocessing.Pool(processes=n)
    pool.map(worker, wordChoicesList)


def worker(words):
    gameState = Wordle()
    maxSteps = 0
    longestGuesses = []
    finalResult = ""
    gameState.setTarget("APPLE")

    agent = SimpleAgent()

    nextGameStates = [gameState.step(word) for word in words]

    while nextGameStates:
        nextGameState = nextGameStates.pop()
        words, count = agent.getAction(nextGameState)
        for word in words:
            nextNextGameState = nextGameState.step(word)
            # debug message
            result_str = ""
            guesses = nextNextGameState.guesses
            for i, gw in enumerate(guesses):
                if (i != len(guesses)-1):
                    result_str += (gw + "->")
                else:
                    result_str += gw
            print(result_str)

            if nextNextGameState.finished:
                if len(nextNextGameState.guesses) > maxSteps:
                    maxSteps = len(nextNextGameState.guesses)
                    longestGuesses = nextNextGameState.guesses
                    print("Longest Length: ", maxSteps)
                    finalResult = result_str
            else:
                nextGameStates.append(nextNextGameState)
    
    print(f" *** Final Longest Length: {maxSteps} *** ")
    print(finalResult)
    print(longestGuesses)


if __name__ == "__main__":
    gameState = Wordle()
    wordChoices = gameState.WORDLIST
    maxSteps = 0
    longestGuesses = []
    gameState.setTarget("APPLE")

    # agent = HeuristicAgent()
    agent = SimpleAgent()

    words, count = agent.getAction(gameState)
    nextGameStates = [gameState.step(word) for word in words]


    

    while nextGameStates:
        nextGameState = nextGameStates.pop()
        words, count = agent.getAction(nextGameState)
        for word in words:
            nextNextGameState = nextGameState.step(word)
            # debug message
            result_str = ""
            guesses = nextNextGameState.guesses
            for i, gw in enumerate(guesses):
                if (i != len(guesses)-1):
                    result_str += (gw + "->")
                else:
                    result_str += gw
            print(result_str)

            if nextNextGameState.finished:
                if len(nextNextGameState.guesses) > maxSteps:
                    maxSteps = len(nextNextGameState.guesses)
                    longestGuesses = nextNextGameState.guesses
                    print("Longest Length: ", maxSteps)
            else:
                nextGameStates.append(nextNextGameState)

    print(longestGuesses)
    print(len(longestGuesses))


