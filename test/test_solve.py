import unittest
from solve import Tile, Word, Board


class Test_Tile(unittest.TestCase):

    def test_validation_fails_1(self):
        inputs = [-1, -1, "a", ["1"]]
        self.assertRaises(ValueError, Tile, *inputs)

    def test_validation_fails_2(self):
        inputs = [1, 2, "aa", ["1"]]
        self.assertRaises(ValueError, Tile, *inputs)

    def test_validation_fails_3(self):
        inputs = [1, 2, "abc", ["1"]]
        self.assertRaises(ValueError, Tile, *inputs)

    def test_repr_loading(self):
        inputs = [1, 2, "a", ["1", "2"]]
        tile = Tile(*inputs)
        self.assertEqual(tile, eval(repr(tile)))


class Test_Word(unittest.TestCase):

    def test_word_repr(self):
        inputs = [
            Tile(0, 0, "a", ["1"]),
            Tile(0, 1, "n", ["1"]),
            Tile(0, 2, "t", ["1"]),
        ]
        word = Word(inputs)
        self.assertEqual(word.get_word(), "ant")

    def test_get_owning_player_1(self):
        inputs = [
            Tile(0, 0, "a", ["1"]),
            Tile(0, 1, "n", ["1"]),
            Tile(0, 2, "t", ["1"]),
        ]
        word = Word(inputs)
        self.assertEqual(word.get_owning_player(), "1")

    def test_get_owning_player_2(self):
        inputs = [
            Tile(0, 0, "a", ["1", "2"]),
            Tile(0, 1, "n", ["1"]),
            Tile(0, 2, "t", ["1"]),
        ]
        word = Word(inputs)
        self.assertEqual(word.get_owning_player(), "1")

    def test_get_owning_player_3(self):
        inputs = [
            Tile(0, 0, "a", ["1", "2"]),
            Tile(0, 1, "n", ["2"]),
            Tile(0, 2, "t", ["2"]),
        ]
        word = Word(inputs)
        self.assertEqual(word.get_owning_player(), "2")

    def test_get_owning_player_4(self):
        inputs = [
            Tile(0, 0, "a", ["1", "2"]),
            Tile(0, 1, "n", ["1", "2"]),
            Tile(0, 2, "t", ["1", "2"]),
        ]
        word = Word(inputs)
        self.assertEqual(word.get_owning_player(), None)

    def test_get_score(self):
        inputs = [
            Tile(0, 0, "a", ["1"]),
            Tile(0, 1, "n", ["1"]),
            Tile(0, 2, "t", ["1"]),
        ]
        word = Word(inputs)
        self.assertEqual(word.get_score(), 3)


class Test_Board(unittest.TestCase):

    def test_board_walking_1(self):
        inputs = [
            [1, 1, "a", ["1"]],
            [1, 2, "n", ["1"]],
            [1, 3, "t", ["1"]],
        ]
        tiles = [
            Tile(0, 0, "a", ["1"]),
            Tile(0, 1, "n", ["1"]),
            Tile(0, 2, "t", ["1"]),
        ]
        words = {
            Word(tiles)
        }
        board = Board(inputs)
        self.assertEqual(board.walk_board(), words)

    def test_board_walking_2(self):
        inputs = [
            [1, 1, "a", ["1"]],
            [2, 1, "n", ["1"]],
            [3, 1, "t", ["1"]],
        ]
        tiles = [
            Tile(0, 0, "a", ["1"]),
            Tile(1, 0, "n", ["1"]),
            Tile(2, 0, "t", ["1"]),
        ]
        words = {
            Word(tiles)
        }
        board = Board(inputs)
        self.assertEqual(board.walk_board(), words)

    def test_board_walking_3(self):
        inputs = [
            [13, 1, "a", ["1"]],
            [14, 1, "n", ["1"]],
            [15, 1, "t", ["1"]],
        ]
        tiles = [
            Tile(12, 0, "a", ["1"]),
            Tile(13, 0, "n", ["1"]),
            Tile(14, 0, "t", ["1"]),
        ]
        words = {
            Word(tiles)
        }
        board = Board(inputs)
        self.assertEqual(board.walk_board(), words)

    def test_board_walking_4(self):
        inputs = [
            [13, 1, "a", ["1"]],
            [14, 1, "n", ["1"]],
            [15, 1, "t", ["1"]],
        ]
        board = Board(inputs)
        scores = {"1": 3}
        self.assertEqual(board.calculate_scores(), scores)

    def test_board_walking_5(self):
        inputs = [
            [1, 1, "a", ["1"]],
            [2, 1, "n", ["1"]],
            [3, 1, "t", ["1", "2"]],
            [3, 2, "i", ["2"]],
            [3, 3, "n", ["2"]],
            [3, 4, "y", ["2"]],
        ]
        board = Board(inputs)
        scores = {"1": 3, "2": 7}
        self.assertEqual(board.calculate_scores(), scores)

if __name__ == "__main__":
    unittest.main()