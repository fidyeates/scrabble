import json
from config import Letters, _SCRIPT_DIR_
from collections import defaultdict
import string

# Letter score lookup
Letters = Letters.from_default_config()


class Tile(object):

    def __init__(self, x, y, letter, players):
        """

        :param int x: The x position of the Tile
        :param int y: The y position of the Tile
        :param str letter: The string representation of the letter
        :param list[str] players: A list of players who played this letter
        """
        if x < 0 or y < 0:
            raise ValueError(f"Tile coordinates: {x}:{y} are invalid")
        self.x = int(x)
        self.y = int(y)
        if letter.lower() not in string.ascii_lowercase or len(letter) != 1:
            raise ValueError(f"{letter} is not a valid letter")
        self.letter = letter.lower()
        self.players = players

    def __repr__(self):
        return f"Tile({self.x}, {self.y}, letter={self.letter!r}, players={self.players})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.letter == other.letter and self.players == other.players


class Word(object):

    def __init__(self, tiles):
        """
        The Word object provides functionality relating to scores and players for a collection of tiles.

        :param list[Tile] tiles: A list of the tiles which makes up this word
        """
        self.tiles = tiles

    def get_word(self):
        """
        Gets a string representation of the full word
        :rtype: str
        """
        return ''.join(l.letter for l in self.tiles)

    def __repr__(self):
        return f"Word({self.get_word()!r})"

    def __hash__(self):
        return self.get_word().__hash__()

    def __eq__(self, other):
        return self.get_word() == other.get_word()

    def get_score(self):
        """
        Returns the score for the word
        :rtype: int
        """
        return sum([Letters.get_value(tile.letter) for tile in self.tiles])

    def get_owning_player(self):
        """
        Gets the owning player for the word, should return the string player name or None

        Note: If every letter of a word is used by more than one player, ownership is unknown and this function returns
        None, and this populates the 'unallocated' scores in the output.
        :rtype: str|None
        """
        i = 0
        while True:
            try:
                players = self.tiles[i].players
            except IndexError:
                return None
            if len(players) == 1:
                return players[0]
            i += 1


class Board(object):
    DIMENSIONS = (15, 15)

    def __init__(self, placed_letters):
        """
        The Board object contains all methods for manipulating and calculating the current scores of the scrabble board.

        :param list[int, int, str, list[str]] placed_letters: A list of data points for the boards current state
        """
        self.grid = []
        self.letters = []

        for _ in range(self.DIMENSIONS[0]):
            self.grid.append([None] * self.DIMENSIONS[0])

        for x, y, letter, players in placed_letters:
            tile = Tile(x-1, y-1, letter, players)
            self.letters.append(tile)
            self.grid[x-1][y-1] = tile

    @staticmethod
    def load_from_config(path=_SCRIPT_DIR_ + "/../board.json"):
        """
        Loads a scrabble board state from a provided config file.

        :param str path: The path to a board.json file
        :rtype: Board
        """
        with open(path, "rb") as f:
            return Board(json.loads(f.read()))

    def print_board(self):
        """
        Prints a representation of the board to stdout
        """
        to_join = ["-" * self.DIMENSIONS[0]]
        for row in self.grid:
            to_join.append("".join([ch.letter if ch is not None else " " for ch in row]))

        print("\n".join(to_join))

    def walk_board(self):
        """
        Iterates over the entire board and finds all complete words.

        :rtype: list[Word]
        """
        words = set()

        # Walk Left to right, up to down
        for x in range(0, self.DIMENSIONS[0] - 1):
            for y in range(0, self.DIMENSIONS[1] - 1):
                tile = self.grid[x][y]
                if tile:

                    # Checking if a start of a word
                    if self.grid[x][y + 1]:

                        # If we're already half way through a word don't do anything
                        if not self.grid[x][y - 1]:
                            words.add(self.get_full_word_for_tile(tile, "right"))

                    if self.grid[x + 1][y]:

                        # If we're already half way through a word don't do anything
                        if not self.grid[x - 1][y]:
                            words.add(self.get_full_word_for_tile(tile, "down"))

        return words

    def get_full_word_for_tile(self, tile, direction="right"):
        """
        Iterates over the scrabble board in a certain direction and identifies whole words from a source tile.

        Returns a Word object containing all the tiles which make up the word.

        :param Tile tile: The tile indicating the start of the word
        :param str direction: The direction to iterate in
        :rtype: Word
        """
        tiles = [tile]
        steps = 1

        while True:

            dx = dy = 0
            if direction == "right":
                dy = steps
            if direction == "down":
                dx = steps

            try:
                new_tile = self.grid[tile.x + dx][tile.y + dy]
            except IndexError:
                # Out of bounds
                break

            if new_tile is None:
                break

            tiles.append(new_tile)
            steps += 1

        return Word(tiles)

    def calculate_scores(self):
        """
        Iterates over the scrabble board and calculates the score for the current state of the game
        :rtype: dict[str, int]
        """
        words = self.walk_board()
        player_scores = {}
        for word in words:
            player = word.get_owning_player()
            if player not in player_scores:
                player_scores[player] = 0
            player_scores[player] += word.get_score()
        return player_scores


if __name__ == "__main__":
    board = Board.load_from_config()
    scores = board.calculate_scores()

    print("Board Scores:")
    for player, score in scores.items():
        if player is None:
            print("Unallocated: ", score)
        else:
            print(": ".join([player, str(score)]))
