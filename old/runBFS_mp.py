from wordle import Wordle
import multiprocessing
from tqdm import tqdm
from agents import HeuristicAgent

"""
Leveraging Multi-processing
"""

def breathFirstSearch(n=4):
    assert n > 0, "No. of processes cannot be 0 or negative"
    game = Wordle()
    wordChoices = game.WORDLIST
    if n == 1:
        return worker(wordChoices)
    split = int(len(wordChoices) / n)
    wordChoicesList = []

    for p in range(n-1):
        wordChoicesList.append(wordChoices[p*split:(p+1)*split])
    wordChoicesList.append(wordChoices[(p+1)*split:])
    
    pool = multiprocessing.Pool(processes=n)
    pool.map(worker, wordChoicesList)

def worker(wordChoices, verbose=False):
    # outputs
    longestGuesses = []
    maxSteps = 0
    agent = HeuristicAgent()
    for wordChoice in tqdm(wordChoices):
        gameState = Wordle()
        gameState.setTarget(wordChoice)
        words, _ = agent.getAction(gameState)
        nextGameStates = [gameState.step(word) for word in words]
        while nextGameStates:
            temp = []
            for nextGameState in nextGameStates:
                words, _ = agent.getAction(nextGameState)
                for word in words:
                    nextNextGameState = nextGameState.step(word)
                    if nextNextGameState.finished:
                        if len(nextNextGameState.guesses) > maxSteps:
                            maxSteps = len(nextNextGameState.guesses)
                            longestGuesses = nextNextGameState.guesses
                            print("Longest Length: ", maxSteps)
                            # print result
                            result_str = ""
                            guesses = nextNextGameState.guesses
                            for i, gw in enumerate(guesses):
                                if (i != len(guesses)-1):
                                    result_str += (gw + "->")
                                else:
                                    result_str += gw
                            print(result_str)
                    else:
                        temp.append(nextNextGameState)
            nextGameStates = temp
    print(longestGuesses)
    print(len(longestGuesses))

if __name__ == "__main__":
    breathFirstSearch(10)
