"# spelling-bee-solver" 

This is an extremely simple solver for the NYT game Spelling Bee. There are many English words that are not valid in the game, so this list is roughly sorted by how frequently words appear in various sources. The further down the list you go, the less likely a word is to be valid.

API Usage:
```python
    '''
    POST /solver
    Description:
        Finds words based on the center and other letters provided in the request.  Note that each returned list
        is a set that has already removed duplicates from the smaller lists so the full list can be ordered roughly
        by frequency of use in the English language.
    Request Body:
        {
            "center_letter": "a",   # Required, a single letter
            "other_letters": "bcdefg" # Required, other letters to use (6 letters for Spelling Bee)
        }
    Response:
        200 OK:
        {
            "result": {
                "10k": [...],       # Words from the 10k list
                "30k": [...],       # Words from the 30k list
                "wiki": [...],      # Words from the Wikipedia list
                "full": [...]       # Words from the full list
            }
        }
        400 Bad Request:
        {
            "error": "Invalid input"
        }
    '''
```
