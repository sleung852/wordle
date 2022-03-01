from wordle import Wordle
from agents import RandomAgent, HeuristicAgent

if __name__ == "__main__":
    gameState = Wordle()
    wordChoices = gameState.WORDLIST
    maxSteps = 0
    longestGuesses = []
    gameState.setTarget("APPLE")

    agent = HeuristicAgent()
    # agent = RandomAgent()

    words, count = agent.getAction(gameState)
    nextGameStates = [gameState.step(word) for word in words]
    while nextGameStates:
        temp = []
        for nextGameState in nextGameStates:
            words, count = agent.getAction(nextGameState)
            for word in words:
                nextNextGameState = nextGameState.step(word)
                if nextNextGameState.finished:
                    if len(nextNextGameState.guesses) > maxSteps:
                        maxSteps = len(nextNextGameState.guesses)
                        longestGuesses = nextNextGameState.guesses
                        print("Longest Length: ", maxSteps)
                else:
                    temp.append(nextNextGameState)
        nextGameStates = temp

    print(longestGuesses)
    print(len(longestGuesses))


