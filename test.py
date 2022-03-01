import unittest

from wordle import Wordle
from old.eldrow import Eldrow

def create_wordle_test_case(target="APPLE"):
    gameState = Wordle(hardmode=True)
    gameState.setTarget(target)
    return gameState

class TestWordleGameLogic(unittest.TestCase):
    def test_colours_signals(self):
        # Case 1
        gs = create_wordle_test_case("ROVER")
        gs = gs.step("ERROR")
        self.assertTrue(gs.colours[0]=="Y")
        self.assertTrue(gs.colours[1]=="Y")
        self.assertTrue(gs.colours[2]=="X")
        self.assertTrue(gs.colours[3]=="Y")
        self.assertTrue(gs.colours[4]=="G")
        # Case 2
        gs = create_wordle_test_case("TIGER")
        gs = gs.step("TRACK")
        self.assertTrue(gs.colours[0]=="G")
        self.assertTrue(gs.colours[1]=="Y")
        self.assertTrue(gs.colours[2]=="X")
        self.assertTrue(gs.colours[3]=="X")
        self.assertTrue(gs.colours[4]=="X")

    def test_yellows(self):
        # Case 1
        gs = create_wordle_test_case("ROVER")
        gs = gs.step("ERROR")
        self.assertTrue("E" in gs.yellows[0])
        self.assertTrue("R" in gs.yellows[1])
        self.assertTrue("O" in gs.yellows[3])
        # Case 2
        gs = create_wordle_test_case("TIGER")
        gs = gs.step("TRACK")
        self.assertTrue("R" in gs.yellows[1])

    def test_greys(self):
        # Case 1
        gs = create_wordle_test_case("ROVER")
        gs = gs.step("ERROR")
        self.assertTrue("R" in gs.greys)
        # Case 2
        gs = create_wordle_test_case("TIGER")
        gs = gs.step("TRACK")
        self.assertTrue("A" in gs.greys)
        self.assertTrue("C" in gs.greys)
        self.assertTrue("K" in gs.greys)

    def test_greens(self):
        # Case 1
        gs = create_wordle_test_case("ROVER")
        gs = gs.step("ERROR")
        self.assertTrue(gs.greens[4] == "R")
        # Case 2
        gs = create_wordle_test_case("TIGER")
        gs = gs.step("TRACK")
        self.assertTrue(gs.greens[0] == "T")

    def test_valid_word_hardmode(self):
        """
        Test Cases provided by Jane Street
        """
        gs = create_wordle_test_case("TIGER")
        gs = gs.step("TRACK")
        # must start with T
        self.assertFalse("DIRTY" in gs.validWords)
        # 2nd letter cant be R
        self.assertFalse("TROMP" in gs.validWords)
        # cant contain A
        self.assertFalse("TARDY" in gs.validWords)
        # cant not contain a R
        self.assertFalse("TEPID" in gs.validWords)
        # cannot be the same word
        self.assertFalse("TRACK" in gs.validWords)

        gs = create_wordle_test_case("SANDY")
        gs = gs.step("DADDY")
        self.assertFalse("DANDY" in gs.validWords)

        gs = create_wordle_test_case("SANDY")
        gs = gs.step("DANDY")
        self.assertFalse("DADDY" in gs.validWords)

    def test_grey_duplications(self):
        gs = create_wordle_test_case("ROVER")
        gs = gs.step("ERROR")
        self.assertTrue(gs._isValidWord("ROVER"))

def create_eldorw_test_case(target="APPLE"):
    gameState = Eldrow()
    gameState.setTarget(target)
    return gameState

if __name__ == '__main__':
    unittest.main()

