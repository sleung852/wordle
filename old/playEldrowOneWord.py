from eldrow import gameEngine
import multiprocessing
from itertools import permutations
from tqdm import tqdm

def depthFirstSearchMP(seq_unique=[], n=4):
    assert n > 0, "No. of processes cannot be 0 or negative"

    max_seq = []
    seqs = []
    for i in range(len(seq_unique)):
        seqs.append(seq_unique[i:] + seq_unique[:i])

    for seq in tqdm(seqs):
        game = gameEngine(seq)
        wordChoices = game.legalwords
        if n == 1:
            return worker(0, wordChoices)
        split = int(len(wordChoices) / n)
        wordChoicesList = []
        
        for p in range(n-1):
            wordChoicesList.append(wordChoices[p*split:(p+1)*split])
        wordChoicesList.append(wordChoices[(p+1)*split:])

        pool = multiprocessing.Pool(processes=n)
        result_max_seqs = pool.starmap(worker, zip(wordChoicesList, [seq]*n))
        for result_max_seq in result_max_seqs:
            if len(result_max_seq) > len(max_seq):
                max_seq=result_max_seq

    print("-"*50)
    print("MAX LENGTH:", len(max_seq))
    print("MAX SEQ:", max_seq)
    print("-"*50)

def worker(word_choices, seq):
    max_length = 1
    max_seq = []

    # seq = ['BATCH', 'CATCH', 'HATCH', 'LATCH', 'MATCH', 'PATCH', 'WATCH']

    for word_choice in word_choices:
        current_list = [word_choice] + seq
        gs = gameEngine(current_list)

        # print(gs.legalwords)

        cache = [gs.step(word) for word in gs.legalwords]

        while (len(cache) > 0):
            gameState = cache.pop()
            gameState.prepare()

            wordchoices = gameState.legalwords
            temp = []
            # if finish
            if len(wordchoices) == 0:
                if len(gameState.seq) > max_length:
                    max_length = len(gameState.seq)
                    # print("Max Length:", max_length)
                    # print(gameState.seq)
                    max_seq = gameState.seq

            for word in wordchoices:
                nextGameState = gameState.step(word)
                temp.append(nextGameState)
                
            cache += temp
        #     print(len(cache))
    # print("-"*50)
    # print("MAX LENGTH:", max_length)
    # print("MAX SEQ:", max_seq)
    # print("-"*50)
    return max_seq

if __name__ == "__main__":
    depthFirstSearchMP(['COWER', 'LOWER', 'MOWER', 'POWER', 'ROWER', 'SOWER', 'TOWER'], 8)
    