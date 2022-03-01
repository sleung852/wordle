from copy import deepcopy

class SimpleAgent:
    def getAction(self, gameState):
        gameState._getValidWords()
        return gameState.validWords, len(gameState.validWords)

class HeuristicAgent:
    def getAction(self, gameState):
        gameState._getValidWords()
        if len(gameState.validWords)==1:
            return gameState.validWords, 1
        maxWords = []
        maxOptions = 0
        for word in gameState.validWords:
            tempGameState = deepcopy(gameState)
            nextGameState = tempGameState.step(word)
            if nextGameState.finished:
                continue
            optionsCount = len(nextGameState.validWords)
            # print(f"Potential Max Word: {word} ({optionsCount})")
            if optionsCount > maxOptions:
                maxOptions = optionsCount
                maxWords = [word]
            elif optionsCount == maxOptions:
                maxWords.append(word)
        return maxWords, maxOptions
