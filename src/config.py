"""
Handles the importing of configuration for the scrabble challenge
"""
import json
import os

_SCRIPT_DIR_ = os.path.dirname(os.path.abspath(__file__))


class Letters(object):

    def __init__(self, values):
        """
        A lookup for storing letter score mappings, requires letter scores in the format:

        {
            "value": int,
            "letters": list[str]
        }

        :param list[dict] values: A list of letter score objects
        """
        self._lookup = {}

        for value_dict in values:
            for letter in value_dict.get("letters", []):
                self._lookup[letter.lower()] = value_dict["value"]

    def get_value(self, letter):
        """
        Gets the score value for the provided letter

        :param str letter: The letter to lookup
        :rtype: int
        """
        return self._lookup[letter.lower()]

    @staticmethod
    def from_default_config():
        """
        Loads the letter config from it's default configuration
        :rtype: Letters
        """
        return load_letters()


def load_letters(path=_SCRIPT_DIR_ + "/../letters.json"):
    """
    Loads a letter mapping from the configuration at the provided path

    :param str path: The path to the configuration json file
    :rtype: Letters
    """
    with open(path) as f:
        return Letters(json.loads(f.read()))

