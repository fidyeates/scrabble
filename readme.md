# Scrabble Challenge

Test Coverage: 92%

## Usage
```
python3 src/solve.py
```

### Requirements
- python3

## Assumptions

- The letters with only one player 'owner' determine who gets the score for the word. 

## Edge Cases

- Doesn't consider ordering of played letters:
    - Therefore it wont handle word composition, such as adding an 's' to the end of a word to make it plural.
- There is an edge case where if a player could create multiple words with no spaces between them, such as:

```
A N D
R O A R
T U N A
I N K
S
T
I
C
```

If player 1 played AND, ARTISTIC and TUNA. and player 2 played ROAR and INK, it's very difficult to assign ownership
and calculate scores for NOUN and DANK. As Player 2 should gain scores for both new words. But in its json representation
the ownership of that would be entirely ambiguous.